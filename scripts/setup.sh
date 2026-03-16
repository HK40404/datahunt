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
        echo -e "${YELLOW}警告: config/.env 不存在，请创建并配置 API Key${NC}"
    else
        # 验证必要的环境变量
        source config/.env 2>/dev/null || true
        if [ -z "$OPENAI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
            echo -e "${YELLOW}警告: 未配置 API Key (OPENAI_API_KEY 或 GOOGLE_API_KEY)${NC}"
        fi
    fi

    echo -e "${GREEN}依赖检查通过${NC}"
}

step_start_mysql() {
    echo -e "${GREEN}[2/7]${NC} 启动 MySQL..."
}

step_download_data() {
    echo -e "${GREEN}[3/7]${NC} 下载 BIRD 数据..."
}

step_import_data() {
    echo -e "${GREEN}[4/7]${NC} 导入数据到 MySQL..."
}

step_embed_schema() {
    echo -e "${GREEN}[5/7]${NC} Schema 嵌入..."
}

step_embed_skeleton() {
    echo -e "${GREEN}[6/7]${NC} 骨架嵌入..."
}

step_extract_relation() {
    echo -e "${GREEN}[7/7]${NC} 提取表关系图..."
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
