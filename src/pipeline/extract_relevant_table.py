import argparse
import json
from pathlib import Path

import networkx as nx
import pymysql
from sqlglot import exp, parse_one
from sqlglot.errors import ParseError
from sqlglot.optimizer.scope import build_scope


def _check_table_exists(
    table_name: str,
    db_id: str,
    host: str | None = None,
    user: str | None = None,
    password: str | None = None,
    database: str | None = None,
    port: int = 3306
) -> bool:
    """
    检查表是否在数据库中真实存在

    Args:
        table_name: 表名
        db_id: 数据库ID
        host: 数据库主机地址
        user: 数据库用户名
        password: 数据库密码
        database: 数据库名称（如果提供，优先使用；否则使用db_id）
        port: 数据库端口，默认3306

    Returns:
        如果表存在返回True，否则返回False
    """
    # 如果没有提供数据库配置，无法验证，返回True（不排除）
    if not host or not user or not password:
        return True

    try:
        # 连接数据库（参考ddl_embed_md.py的方式）
        # 不指定database，只连接服务器
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4',
            connect_timeout=5
        )

        try:
            with connection.cursor() as cursor:
                # 检查表是否存在（不验证schema，只检查表名，不区分大小写）
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE LOWER(table_name) = LOWER(%s)",
                    (table_name,)
                )
                result = cursor.fetchone()
                return result[0] > 0
        finally:
            connection.close()
    except Exception:
        # 如果连接失败或查询失败，返回True（不排除，避免误删）
        return True


def extract_join_relationships(
    sql: str,
    db_id: str | None = None,
    host: str | None = None,
    user: str | None = None,
    password: str | None = None,
    database: str | None = None,
    port: int = 3306
) -> tuple[list[tuple[str, str]], set[str]]:
    """
    从SQL语句中提取JOIN关系（排除CTE、子查询和别名）

    使用 sqlglot 的 scope traversal 来正确区分实际数据库表和CTE/子查询/别名
    如果提供了数据库配置，会验证表是否真实存在于数据库中

    Args:
        sql: SQL语句字符串
        db_id: 数据库ID
        host: 数据库主机地址
        user: 数据库用户名
        password: 数据库密码
        database: 数据库名称（如果提供，优先使用；否则使用db_id）
        port: 数据库端口，默认3306

    Returns:
        (JOIN关系列表, 不存在的表集合)的元组
        JOIN关系列表：每个元素为(表1, 表2)的元组，按字母顺序排序
        不存在的表集合：验证时发现数据库中不存在的表名集合
    """
    relationships = []
    missing_tables = set()

    try:
        # 使用 sqlglot 解析 SQL
        # 使用 MySQL 方言，因为数据是 MySQL 格式
        ast = parse_one(sql, dialect="mysql")

        # 使用 scope traversal 来正确提取实际数据库表（排除CTE、子查询和别名）
        root = build_scope(ast)

        # 收集所有提取到的表名，用于后续验证
        all_tables = set()
        temp_relationships = []

        # 一个scope代表一个 SELECT 语句（子查询也是一个scope）
        # 遍历所有 scope，提取实际数据库表之间的JOIN关系
        for scope in root.traverse():
            # selected_sources 包含该 scope 中选择的源（FROM/JOIN 子句中的）
            # 格式: {alias: (node, source)}
            # - alias: 别名（如 FROM users AS u 中的 u）
            # - source: 如果是 exp.Table 实例，说明是实际数据库表
            #           如果是 Scope 实例，说明是子查询或CTE，需要排除
            # 我们提取 source.name（实际表名），而不是 alias（别名）

            # 构建别名/表名到实际表名的映射（只包含实际数据库表）
            # key可以是别名或表名，value是实际表名（小写）
            alias_to_table = {}
            for alias, (node, source) in scope.selected_sources.items():
                if isinstance(source, exp.Table):
                    table_name = source.name
                    if table_name:
                        table_name_lower = table_name.lower()
                        alias_to_table[alias] = table_name_lower
                        all_tables.add(table_name_lower)
                        # 如果别名就是表名本身，也添加映射
                        if alias.lower() != table_name_lower:
                            alias_to_table[table_name_lower] = table_name_lower

            # 如果该scope中没有实际数据库表，跳过
            if not alias_to_table:
                continue

            # 获取该scope对应的SELECT节点
            if scope.expression and isinstance(scope.expression, exp.Select):
                select = scope.expression

                # 获取FROM子句
                from_expr = select.args.get('from_')
                if not from_expr:
                    continue

                # 获取FROM子句对应的source，检查是否是实际数据库表
                from_source = None
                from_alias = None
                if isinstance(from_expr.this, exp.Alias):
                    from_alias = from_expr.this.alias
                    # 从scope.selected_sources中查找对应的source
                    if from_alias in scope.selected_sources:
                        from_source = scope.selected_sources[from_alias][1]
                elif isinstance(from_expr.this, exp.Table):
                    from_alias = from_expr.this.alias or from_expr.this.name
                    if from_alias and from_alias in scope.selected_sources:
                        from_source = scope.selected_sources[from_alias][1]

                # 只有当FROM是实际数据库表时才继续
                if not isinstance(from_source, exp.Table):
                    continue

                # 提取FROM表的实际表名
                from_table = from_source.name.lower() if from_source.name else None
                if not from_table:
                    continue

                # 获取JOIN列表
                joins = select.args.get('joins', [])

                if joins:
                    # 有显式JOIN的情况
                    # JOIN是链式结构：FROM table1 JOIN table2 ON ... JOIN table3 ON ...
                    # 关系链：table1 <-> table2 <-> table3 <-> ...

                    # 第一个JOIN：FROM表 <-> JOIN[0]表
                    prev_table = from_table
                    for join in joins:
                        # 获取JOIN右侧对应的source，检查是否是实际数据库表
                        join_source = None
                        join_alias = None
                        if isinstance(join.this, exp.Alias):
                            join_alias = join.this.alias
                            if join_alias in scope.selected_sources:
                                join_source = scope.selected_sources[join_alias][1]
                        elif isinstance(join.this, exp.Table):
                            join_alias = join.this.alias or join.this.name
                            if join_alias and join_alias in scope.selected_sources:
                                join_source = scope.selected_sources[join_alias][1]

                        # 只有当JOIN的表是实际数据库表时才创建关系
                        if isinstance(join_source, exp.Table):
                            join_table = join_source.name.lower() if join_source.name else None
                            if join_table:
                                # 先收集关系，稍后统一验证
                                table_pair = tuple(sorted([prev_table, join_table]))
                                temp_relationships.append(table_pair)
                                # 当前JOIN的表成为下一个JOIN的左侧表
                                prev_table = join_table

        # 如果提供了数据库配置，验证所有表是否真实存在
        missing_tables = set()
        if db_id and all_tables and host and user and password:
            valid_tables = set()
            for table_name in all_tables:
                if _check_table_exists(
                    table_name, db_id,
                    host=host, user=user, password=password,
                    database=database, port=port
                ):
                    valid_tables.add(table_name)
                else:
                    missing_tables.add(table_name)

            # 只保留两个表都存在的JOIN关系
            for table_pair in temp_relationships:
                table1, table2 = table_pair
                if table1 in valid_tables and table2 in valid_tables:
                    relationships.append(table_pair)
        else:
            # 如果没有提供数据库配置，直接使用所有关系
            relationships = temp_relationships

        # 去重
        relationships = list(set(relationships))

    except (ParseError, Exception):
        # 如果解析失败，不创建关系（只统计JOIN关系）
        # 解析失败可能是因为SQL语法特殊，无法确定是否有JOIN关系
        pass

    return relationships, missing_tables


def extract_table_relationships_from_json(
    json_file: str | Path,
    excluded_question_ids: set[int] | None = None,
    host: str | None = None,
    user: str | None = None,
    password: str | None = None,
    database: str | None = None,
    port: int = 3306
) -> nx.Graph:
    """
    从JSON文件中提取所有SQL的表关联关系，直接构建为networkX图对象（只统计JOIN关系）

    Args:
        json_file: JSON文件路径
        excluded_question_ids: 需要排除的question_id集合，如果为None则从mini_dev_mysql.json加载
        host: 数据库主机地址（如果提供，所有SQL使用此配置）
        user: 数据库用户名（如果提供，所有SQL使用此配置）
        password: 数据库密码（如果提供，所有SQL使用此配置）
        database: 数据库名称（如果提供，所有SQL使用此配置；否则使用每个SQL的db_id）
        port: 数据库端口，默认3306

    Returns:
        networkX无向图对象，节点为表名，边权重为出现次数
    """
    json_path = Path(json_file)
    if not json_path.exists():
        raise FileNotFoundError(f"文件不存在: {json_path}")

    # 如果没有提供排除列表，尝试从mini_dev_mysql.json加载
    if excluded_question_ids is None:
        excluded_question_ids = set()
        mini_dev_file = Path(__file__).parent / "data" / "mini_dev_mysql.json"
        if mini_dev_file.exists():
            try:
                with open(mini_dev_file, encoding='utf-8') as f:
                    mini_data = json.load(f)
                excluded_question_ids = set(
                    item.get('question_id')
                    for item in mini_data
                    if 'question_id' in item
                )
                print(f"📋 从 {mini_dev_file} 加载了 {len(excluded_question_ids)} 个需要排除的question_id")
            except Exception as e:
                print(f"⚠️  无法加载排除列表: {e}")

    # 读取JSON文件
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    # 直接构建networkX图对象
    G = nx.Graph()
    # 用于统计边的权重（出现次数）
    edge_weights = {}
    # 收集所有不存在的表
    all_missing_tables = set()

    total_sqls = len(data)
    excluded_count = 0
    processed_count = 0

    print(f"📊 开始处理 {total_sqls} 条SQL语句...")
    if excluded_question_ids:
        print(f"   排除 {len(excluded_question_ids)} 个question_id")

    for idx, item in enumerate(data, 1):
        # 检查是否需要排除
        question_id = item.get('question_id')
        if question_id is not None and question_id in excluded_question_ids:
            excluded_count += 1
            continue

        sql = item.get('SQL', '')
        if not sql:
            continue

        # 获取db_id用于表验证
        db_id = item.get('db_id')

        # 提取JOIN关系（只统计JOIN关系）
        relationships, missing_tables = extract_join_relationships(
            sql,
            db_id=db_id,
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )

        # 收集不存在的表
        all_missing_tables.update(missing_tables)

        # 只处理有JOIN关系的情况
        if relationships:
            processed_count += 1
            # 直接添加到图中
            for table1, table2 in relationships:
                # 添加节点
                G.add_node(table1)
                G.add_node(table2)

                # 统计边的权重
                edge_key = tuple(sorted([table1, table2]))
                if edge_key in edge_weights:
                    edge_weights[edge_key] += 1
                else:
                    edge_weights[edge_key] = 1

        # 显示进度
        if idx % 100 == 0:
            progress = (idx / total_sqls) * 100
            print(f"  进度: [{idx}/{total_sqls}] ({progress:.1f}%) - 已处理: {processed_count}, 已排除: {excluded_count}")

    # 添加边和权重
    for (table1, table2), weight in edge_weights.items():
        G.add_edge(table1, table2, weight=weight)

    print(f"✅ 处理完成，共分析了 {total_sqls} 条SQL语句")
    print(f"   - 排除: {excluded_count} 条")
    print(f"   - 有JOIN关系: {processed_count} 条")
    print(f"   - 无JOIN关系: {total_sqls - excluded_count - processed_count} 条")
    print(f"   - 图对象: {G.number_of_nodes()} 个节点, {G.number_of_edges()} 条边")

    # 打印不存在的表
    if all_missing_tables:
        print(f"\n⚠️  数据库中不存在的表（共 {len(all_missing_tables)} 个）:")
        for table_name in sorted(all_missing_tables):
            print(f"   - {table_name}")

    return G


def print_table_relationships(G: nx.Graph, top_n: int = 10, max_tables: int = 5):
    """
    打印表关联关系统计结果

    Args:
        G: networkX图对象
        top_n: 每个表显示前N个最常关联的表
        max_tables: 最多显示多少个表的统计结果，默认5
    """
    print(f"\n{'='*80}")
    print("表关联关系统计结果")
    print(f"{'='*80}\n")

    # 按节点的度（关联表数量）排序
    nodes_by_degree = sorted(
        G.nodes(),
        key=lambda n: G.degree(n),
        reverse=True
    )

    # 只展示前5条
    for table_name in nodes_by_degree[:5]:
        # 获取该表的所有邻居及其边的权重
        neighbors = list(G.neighbors(table_name))
        if not neighbors:
            continue

        # 按边的权重排序
        neighbor_weights = [
            (neighbor, G[table_name][neighbor].get('weight', 0))
            for neighbor in neighbors
        ]
        sorted_neighbors = sorted(
            neighbor_weights,
            key=lambda x: x[1],
            reverse=True
        )

        print(f"📋 表: {table_name}")
        print(f"   关联表数量: {len(neighbors)}")
        print(f"   前{top_n}个最常关联的表:")

        for related_table, weight in sorted_neighbors[:top_n]:
            print(f"     - {related_table}: {weight} 次")

        print()


def save_table_relationships(G: nx.Graph, output_file: str | Path):
    """
    将networkX图对象保存为networkX的JSON格式

    Args:
        G: networkX图对象
        output_file: 输出文件路径
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 使用networkX的node_link_data转换为JSON格式
    graph_data = nx.node_link_data(G)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 图对象已保存到: {output_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='提取表关系')
    parser.add_argument('--input', type=str, default=None, help='输入的JSON文件路径')
    parser.add_argument('--output', type=str, default=None, help='输出的JSON文件路径')
    parser.add_argument('--host', type=str, default=None, help='MySQL主机地址')
    parser.add_argument('--user', type=str, default=None, help='MySQL用户名')
    parser.add_argument('--password', type=str, default=None, help='MySQL密码')
    parser.add_argument('--database', type=str, default=None, help='数据库名')
    parser.add_argument('--port', type=int, default=3306, help='MySQL端口')
    args = parser.parse_args()

    # 修改输入文件路径
    if args.input:
        input_file = args.input
    else:
        input_file = Path(__file__).parent.parent.parent / "data" / "dev_20240627" / "dev.json"

    # 修改输出文件路径
    if args.output:
        output_file = args.output
    else:
        output_file = Path(__file__).parent / "output" / "table_relation" / "table_relationships.json"

    # 数据库配置
    host = args.host or '127.0.0.1'
    user = args.user or 'root'
    password = args.password or '123'
    database = args.database or 'bird'
    port = args.port

    # 直接提取为networkX图对象（带数据库验证）
    G = extract_table_relationships_from_json(
        input_file,
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )

    # 打印统计结果（只展示前5条）
    print_table_relationships(G, top_n=10, max_tables=5)

    # 保存为networkX的JSON格式
    save_table_relationships(G, output_file)

