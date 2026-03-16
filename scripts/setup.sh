#!/bin/bash
set -e

# ===========================================
# DataHunt 一键安装脚本
# ===========================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认选项
SKIP_MYSQL=false
SKIP_DATA=false
SKIP_EMBED=false
REBUILD=false

# 显示帮助
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --skip-mysql    跳过 MySQL 容器启动"
    echo "  --skip-data     跳过 BIRD 数据下载和导入"
    echo "  --skip-embed    跳过嵌入生成"
    echo "  --rebuild       重建所有（删除已有数据）"
    echo "  --help          显示帮助"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-mysql)
            SKIP_MYSQL=true
            shift
            ;;
        --skip-data)
            SKIP_DATA=true
            shift
            ;;
        --skip-embed)
            SKIP_EMBED=true
            shift
            ;;
        --rebuild)
            REBUILD=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 步骤函数
step_check_deps() {
    echo -e "${GREEN}[1/7]${NC} 检查依赖..."

    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: Docker 未安装${NC}"
        echo "请访问 https://www.docker.com/get-started 安装 Docker"
        exit 1
    fi

    # 检查 Docker 是否运行
    if ! docker info &> /dev/null; then
        echo -e "${RED}错误: Docker 未运行${NC}"
        echo "请启动 Docker Desktop 或 docker 服务"
        exit 1
    fi

    # 检查 uv
    if ! command -v uv &> /dev/null; then
        echo -e "${RED}错误: uv 未安装${NC}"
        echo "请运行: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi

    # 检查 Python 版本
    if ! command -v python &> /dev/null; then
        echo -e "${RED}错误: Python 未安装${NC}"
        exit 1
    fi
    PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    REQUIRED_VERSION="3.13"
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
        echo -e "${RED}错误: Python 版本需要 3.13+，当前版本: $PYTHON_VERSION${NC}"
        exit 1
    fi

    # 检查 .env 配置
    if [ ! -f "config/.env" ]; then
        echo -e "${YELLOW}警告: config/.env 不存在，正在创建模板文件...${NC}"
        mkdir -p config
        cat > config/.env << 'EOF'
# 请配置你的 API Key
# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# Gemini API Key (可选)
GEMINI_API_KEY=your-gemini-api-key-here

# LangSmith API Key (可选，用于链路追踪)
LANGSMITH_API_KEY=

# 以下为内部使用的 API Key 变量，通常与 OPENAI_API_KEY 相同
SQL_API_KEY=
SKELETON_EXTRACTOR_API_KEY=
REWRITE_API_KEY=
EOF
        echo -e "${YELLOW}已创建 config/.env 模板文件，请编辑并配置你的 API Key${NC}"
        echo -e "${YELLOW}注意: 未配置 API Key，部分功能将无法使用${NC}"
    else
        # 验证必要的环境变量
        source config/.env 2>/dev/null || true
        if [ -z "$OPENAI_API_KEY" ] && [ -z "$GEMINI_API_KEY" ]; then
            echo -e "${YELLOW}警告: 未配置 API Key (OPENAI_API_KEY 或 GEMINI_API_KEY)${NC}"
        fi
    fi

    echo -e "${GREEN}依赖检查通过${NC}"
}

# 数据迁移：移动现有数据文件到新位置
migrate_data() {
    echo "检查数据迁移..."

    # 迁移 field_desc
    if [ -d "src/pipeline/data/field_desc" ] && [ ! -d "data/field_desc" ]; then
        echo "迁移 field_desc..."
        mkdir -p data
        mv src/pipeline/data/field_desc data/
    fi

    # 迁移 mini_dev_mysql.json
    if [ -f "src/pipeline/data/mini_dev_mysql.json" ] && [ ! -f "data/bird/mini_dev_mysql.json" ]; then
        echo "迁移 mini_dev_mysql.json..."
        mkdir -p data/bird
        mv src/pipeline/data/mini_dev_mysql.json data/bird/
    fi
}

step_start_mysql() {
    echo -e "${GREEN}[2/7]${NC} 启动 MySQL..."

    # 如果是 rebuild 模式，先删除已有容器
    if [ "$REBUILD" = "true" ]; then
        echo "重建模式，删除已有 MySQL 容器..."
        docker rm -f datahunt-mysql 2>/dev/null || true
    fi

    # 检查容器是否已存在
    if docker ps -a --format '{{.Names}}' | grep -q "^datahunt-mysql$"; then
        if docker ps --format '{{.Names}}' | grep -q "^datahunt-mysql$"; then
            echo "MySQL 容器已在运行"
            return 0
        else
            echo "MySQL 容器已存在但未运行，启动它..."
            docker start datahunt-mysql
            sleep 10
            return 0
        fi
    fi

    # 创建 MySQL 容器
    echo "创建 MySQL 容器..."
    docker run -d \
        --name datahunt-mysql \
        -e MYSQL_ROOT_PASSWORD=123 \
        -e MYSQL_DATABASE=bird \
        -p 3306:3306 \
        mysql:8.0

    # 等待 MySQL 就绪
    echo "等待 MySQL 启动..."
    local max_attempts=60
    local attempt=0
    while [ $attempt -lt $max_attempts ]; do
        # 先等待更长时间让 MySQL 初始化
        if [ $attempt -lt 15 ]; then
            sleep 2
            attempt=$((attempt + 1))
            continue
        fi
        if docker exec datahunt-mysql mysqladmin ping -h localhost -u root -p123 &> /dev/null; then
            # 启用 LOCAL INFILE 用于 CSV 导入
            docker exec datahunt-mysql mysql -u root -p123 -e "SET GLOBAL local_infile = 1;" 2>/dev/null || true
            echo -e "${GREEN}MySQL 已就绪${NC}"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 2
    done

    echo -e "${RED}错误: MySQL 启动超时${NC}"
    exit 1
}

step_download_data() {
    echo -e "${GREEN}[3/7]${NC} 下载 BIRD 数据..."

    local data_dir="data/bird/mini_dev"
    local mysql_dump="data/bird/minidev/MINIDEV_mysql/BIRD_dev.sql"
    local mini_dev_url="https://drive.usercontent.google.com/download?id=13VLWIwpw5E3d5DUkMvzw7hvHE67a4XkG&export=download&authuser=0&confirm=t&uuid=96307f8f-f525-40f2-bc81-5a644744d750&at=AGN2oQ0JHauUIyibFkkblxj4FYgI:1773651631781"

    # 如果 MySQL dump 已存在且不是 rebuild 模式，跳过下载
    if [ -f "$mysql_dump" ] && [ "$REBUILD" = "false" ]; then
        echo "BIRD MySQL 数据已存在，跳过下载"
        return 0
    fi

    # 如果是 rebuild 模式，删除旧数据
    if [ "$REBUILD" = "true" ]; then
        echo "重建模式，删除旧数据..."
        rm -rf data/bird
    fi

    # 创建目录
    mkdir -p data/bird

    # 下载 mini_dev 数据集
    echo "下载 BIRD mini_dev 数据集..."
    if [ ! -f "data/bird/minidev.zip" ]; then
        curl -L -o "data/bird/minidev.zip" "$mini_dev_url" --retry 3 --connect-timeout 60
    fi

    # 解压
    echo "解压数据..."
    unzip -o "data/bird/minidev.zip" -d "data/bird/"
    rm -f "data/bird/minidev.zip"

    echo -e "${GREEN}BIRD 数据下载完成${NC}"
}

step_import_data() {
    echo -e "${GREEN}[4/7]${NC} 导入数据到 MySQL..."

    # 直接使用官方的 MySQL dump 文件
    local sql_file="data/bird/minidev/MINIDEV_mysql/BIRD_dev.sql"

    # 检查数据文件是否存在
    if [ ! -f "$sql_file" ]; then
        echo -e "${RED}错误: MySQL 数据文件不存在: $sql_file${NC}"
        echo "请先运行数据下载步骤"
        exit 1
    fi

    echo "使用 MySQL 数据文件: $sql_file"

    # 直接导入官方的 MySQL dump 文件
    echo "导入数据到 MySQL（这可能需要几分钟）..."
    docker exec -i datahunt-mysql mysql -u root -p123 bird < "$sql_file"

    echo -e "${GREEN}数据导入完成${NC}"
}

step_embed_schema() {
    echo -e "${GREEN}[5/7]${NC} Schema 嵌入..."

    # 检查 uv 依赖
    if [ ! -d ".venv" ]; then
        echo "安装 Python 依赖..."
        uv sync
    fi

    # 设置 PYTHONPATH 以便导入 src 模块
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

    # 导出 schema 并嵌入
    echo "运行 ddl_embed_md.py..."
    PYTHONPATH="$PROJECT_DIR/src" .venv/bin/python src/pipeline/ddl_embed_md.py \
        --host 127.0.0.1 \
        --port 3306 \
        --user root \
        --password 123 \
        --database bird \
        --output output/rag_schema.sql \
        --collection bird

    echo -e "${GREEN}Schema 嵌入完成${NC}"
}

step_embed_skeleton() {
    echo -e "${GREEN}[6/7]${NC} 骨架嵌入..."

    # 设置 PYTHONPATH
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

    # 查找问题 JSON 文件
    local input_json=""
    for f in data/bird/minidev/MINIDEV/*.json; do
        if [ -f "$f" ]; then
            input_json="$f"
            break
        fi
    done

    if [ -z "$input_json" ]; then
        echo -e "${YELLOW}警告: 未找到问题数据文件，跳过骨架嵌入${NC}"
        return 0
    fi

    echo "运行 extract_question_skeleton.py..."
    PYTHONPATH="$PROJECT_DIR/src" .venv/bin/python -m src.pipeline.extract_question_skeleton \
        --input "$input_json" \
        --clear

    echo -e "${GREEN}骨架嵌入完成${NC}"
}

step_extract_relation() {
    echo -e "${GREEN}[7/7]${NC} 提取表关系图..."

    # 设置 PYTHONPATH
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

    # 查找问题 JSON 文件
    local input_json=""
    for f in data/bird/minidev/MINIDEV/*.json; do
        if [ -f "$f" ]; then
            input_json="$f"
            break
        fi
    done

    if [ -z "$input_json" ]; then
        echo -e "${YELLOW}警告: 未找到问题数据文件，跳过关系图提取${NC}"
        return 0
    fi

    # 创建输出目录
    mkdir -p output/table_relation

    echo "运行 extract_relevant_table.py..."
    PYTHONPATH="$PROJECT_DIR/src" .venv/bin/python -m src.pipeline.extract_relevant_table \
        --input "$input_json" \
        --output "output/table_relation/table_relationships.json"

    echo -e "${GREEN}关系图提取完成${NC}"
}

# 主流程
main() {
    echo "==========================================="
    echo "DataHunt 本地开发环境安装"
    echo "==========================================="

    # 步骤 1: 检查依赖（只有全部跳过才不检查）
    if $SKIP_MYSQL && $SKIP_DATA && $SKIP_EMBED; then
        echo "所有步骤已跳过"
    else
        step_check_deps
    fi

    # 数据迁移
    migrate_data

    # 步骤 2: 启动 MySQL
    if ! $SKIP_MYSQL; then
        step_start_mysql
    fi

    # 步骤 3: 下载数据
    if ! $SKIP_DATA; then
        step_download_data
    fi

    # 步骤 4: 导入数据
    if ! $SKIP_DATA; then
        step_import_data
    fi

    # 步骤 5: Schema 嵌入
    if ! $SKIP_EMBED; then
        step_embed_schema
    fi

    # 步骤 6: 骨架嵌入
    if ! $SKIP_EMBED; then
        step_embed_skeleton
    fi

    # 步骤 7: 关系图
    if ! $SKIP_EMBED; then
        step_extract_relation
    fi

    echo -e "${GREEN}===========================================${NC}"
    echo -e "${GREEN}安装完成！${NC}"
    echo -e "${GREEN}===========================================${NC}"
}

main "$@"
