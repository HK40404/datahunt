"""
问题提取模块

从JSON文件中提取问题、evidence和SQL中涉及的表名，用于RAG基准测试。
"""

import argparse
import json
from pathlib import Path

from sqlglot import exp, parse_one
from sqlglot.errors import ParseError
from sqlglot.optimizer.scope import build_scope


def extract_tables_from_sql(sql: str) -> list[str]:
    """
    从SQL语句中提取涉及的表名（排除CTE、临时结果集和别名）

    使用 sqlglot 的 scope traversal 来正确区分实际数据库表和CTE/子查询/别名

    Args:
        sql: SQL语句字符串

    Returns:
        表名列表（去重后，小写），只包含实际数据库表名，不包含别名
    """
    try:
        # 使用 sqlglot 解析 SQL
        # 使用 MySQL 方言，因为数据是 MySQL 格式
        ast = parse_one(sql, dialect="mysql")

        # 使用 scope traversal 来正确提取实际数据库表（排除CTE、子查询和别名）
        root = build_scope(ast)
        tables = set()

        # 遍历所有 scope，提取实际数据库表
        for scope in root.traverse():
            # selected_sources 包含该 scope 中选择的源（FROM/JOIN 子句中的）
            # 格式: {alias: (node, source)}
            # - alias: 别名（如 FROM users AS u 中的 u）
            # - source: 如果是 exp.Table 实例，说明是实际数据库表
            #           如果是 Scope 实例，说明是子查询或CTE，需要排除
            # 我们提取 source.name（实际表名），而不是 alias（别名）
            for alias, (node, source) in scope.selected_sources.items():
                if isinstance(source, exp.Table):
                    table_name = source.name
                    if table_name:
                        tables.add(table_name.lower())

        return sorted(list(tables))

    except (ParseError, Exception) as e:
        # 如果解析失败，返回空列表
        # 在实际应用中，可以记录错误日志
        print(f"⚠️  SQL解析失败: {e}")
        print(f"   SQL: {sql}")
        return []


def extract_questions_from_json(json_file: str | Path) -> list[dict]:
    """
    从JSON文件中提取每个问题的question、evidence和SQL中涉及的表

    Args:
        json_file: JSON文件路径

    Returns:
        包含question、evidence、tables的字典列表
    """
    json_path = Path(json_file)
    if not json_path.exists():
        raise FileNotFoundError(f"文件不存在: {json_path}")

    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for item in data:
        question = item.get('question', '')
        evidence = item.get('evidence', '')
        sql = item.get('SQL', '')
        question_id = item.get('question_id')
        db_id = item.get('db_id')

        # 提取SQL中涉及的表
        tables = extract_tables_from_sql(sql)

        results.append({
            'question_id': question_id,
            'db_id': db_id,
            'question': question,
            'evidence': evidence,
            'ground_truth_tables': tables,
            'sql': sql  # 保留SQL以便验证
        })

    return results


def main():
    """主函数：处理命令行参数并执行提取"""
    parser = argparse.ArgumentParser(
        description="从JSON文件中提取问题、evidence和SQL中涉及的表名",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 使用默认路径
  python src/pipeline/extract_question.py

  # 指定输入和输出文件
  python src/pipeline/extract_question.py --input data/input.json --output output/questions.json
        """
    )

    parser.add_argument(
        '--input',
        type=str,
        help='输入的JSON文件路径（默认: data/mini_dev_mysql.json）'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='输出的JSON文件路径（默认: output/question_tables_extracted.json）'
    )

    args = parser.parse_args()

    # 默认值
    pipeline_dir = Path(__file__).resolve().parent
    data_dir = pipeline_dir / "data"
    output_dir = pipeline_dir / "output"

    input_file = Path(args.input) if args.input else data_dir / "mini_dev_mysql.json"
    output_file = Path(args.output) if args.output else output_dir / "question_tables_extracted.json"

    # 检查输入文件是否存在
    if not input_file.exists():
        print(f"❌ 输入文件不存在: {input_file}")
        return

    # 执行提取
    print(f"📊 正在从 {input_file} 提取数据...")
    results = extract_questions_from_json(input_file)

    print(f"\n✅ 成功提取 {len(results)} 个问题")

    # 显示前5个示例
    print("\n前5个示例:")
    for i, result in enumerate(results[:5], 1):
        print(f"\n--- 示例 {i} ---")
        print(f"Question ID: {result['question_id']}")
        print(f"DB ID: {result['db_id']}")
        print(f"Question: {result['question']}")
        print(f"Evidence: {result['evidence']}")
        print(f"Tables: {result['ground_truth_tables']}")

    # 统计信息
    total_tables = sum(len(r['ground_truth_tables']) for r in results)
    avg_tables = total_tables / len(results) if results else 0
    print("\n📊 统计信息:")
    print(f"  总问题数: {len(results)}")
    print(f"  平均每个问题涉及的表数: {avg_tables:.2f}")

    # 保存结果
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存到: {output_file.absolute()}")


if __name__ == "__main__":
    main()
