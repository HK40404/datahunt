import argparse
import csv
import json
import uuid
from pathlib import Path

import pymysql

from embed.bge_embedder import BGEEmbedder
from vectordb.metadata import SchemaMetadata
from vectordb.milvus import MilvusWrapper


def load_table_db_mapping() -> dict[str, str]:
    """
    从 dev_tables.json 加载表名到数据库ID的映射

    Returns:
        字典，key为表名（小写），value为数据库ID
    """
    mapping = {}

    # 尝试多个可能的路径
    possible_paths = [
        Path(__file__).parent.parent / "data" / "bird" / "minidev" / "MINIDEV" / "dev_tables.json",
        Path.cwd() / "data" / "bird" / "minidev" / "MINIDEV" / "dev_tables.json",
    ]

    for json_path in possible_paths:
        if json_path.exists():
            try:
                with open(json_path, encoding='utf-8') as f:
                    data = json.load(f)
                for item in data:
                    db_id = item.get('db_id', '')
                    table_names = item.get('table_names', [])
                    for table_name in table_names:
                        mapping[table_name.lower()] = db_id
                print(f"📋 已加载 {len(mapping)} 个表到数据库的映射关系")
                return mapping
            except Exception as e:
                print(f"⚠️  无法加载 dev_tables.json: {e}")

    return mapping


def load_field_descriptions(
    table_name: str,
    database: str,
    table_db_mapping: dict[str, str] = None
) -> dict[str, tuple[str, str]]:
    """
    从CSV文件加载字段描述和data_format

    Args:
        table_name: 表名
        database: 当前数据库名
        table_db_mapping: 表名到数据库ID的映射

    Returns:
        字典，key为字段名（original_column_name，小写），value为(column_description, data_format)的元组
    """
    field_info = {}

    # 尝试多个可能的路径
    possible_base_dirs = [
        Path(__file__).parent.parent / "data" / "bird" / "minidev" / "MINIDEV" / "dev_databases",
        Path.cwd() / "data" / "bird" / "minidev" / "MINIDEV" / "dev_databases",
    ]

    field_desc_base_dir = None
    for base_dir in possible_base_dirs:
        if base_dir.exists():
            field_desc_base_dir = base_dir
            break

    if field_desc_base_dir is None:
        return field_info
    # 根据表名确定数据库ID
    db_id = None
    if table_db_mapping:
        db_id = table_db_mapping.get(table_name.lower())
    if not db_id:
        db_id = database

    # 查找数据库对应的 description 目录
    db_desc_dir = field_desc_base_dir / db_id / "database_description"

    if not db_desc_dir.exists():
        return field_info

    # 尝试多种文件名变体
    possible_names = [
        table_name,
        table_name.lower(),
        table_name.capitalize(),
        table_name.title(),
    ]

    csv_path = None
    for name in possible_names:
        test_path = db_desc_dir / f"{name}.csv"
        if test_path.exists():
            csv_path = test_path
            break

    if csv_path is None:
        return field_info

    # 尝试多种编码（优先使用utf-8-sig来处理BOM）
    encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb18030', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(csv_path, encoding=encoding) as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # 获取字段值，处理可能的BOM问题
                    original_column_name = row.get('original_column_name', '').strip()
                    # 如果获取不到，尝试带BOM的字段名
                    if not original_column_name:
                        original_column_name = row.get('\ufefforiginal_column_name', '').strip()

                    column_description = row.get('column_description', '').strip()
                    if not column_description:
                        column_description = row.get('\ufeffcolumn_description', '').strip()

                    data_format = row.get('data_format', '').strip()
                    if not data_format:
                        data_format = row.get('\ufeffdata_format', '').strip()

                    if original_column_name:
                        # 使用小写作为key，以便大小写不敏感匹配
                        field_info[original_column_name.lower()] = (column_description, data_format)
                # 如果成功读取，跳出循环
                break
        except UnicodeDecodeError:
            # 如果编码错误，尝试下一个编码
            continue
        except Exception as e:
            print(f"⚠️  读取字段描述文件 {csv_path} 时出错: {e}")
            break

    return field_info


def export_schema_for_rag(host, user, password, database, output_file, port: int = 3306):
    """
    导出数据库Schema信息

    Returns:
        tuple: (rag_contents: list[str], table_metas: list[SchemaMetadata])
    """
    # 加载表到数据库的映射关系
    table_db_mapping = load_table_db_mapping()

    try:
        print(f"正在连接 MySQL 数据库: {host}:{port}/{database}")
        connection = pymysql.connect(
            host=host, port=port, user=user, password=password, database=database,
            charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
        print(f"✅ 成功连接到 MySQL 数据库: {host}:{port}/{database}")

        rag_contents = []
        table_metas: list[SchemaMetadata] = []

        with connection.cursor() as cursor:
            # 1. 获取所有表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if not tables:
                return
            table_key = list(tables[0].keys())[0]
            total_tables = len(tables)

            for idx, table_dict in enumerate(tables, 1):
                table_name = table_dict[table_key]

                # 显示进度信息
                progress = (idx / total_tables) * 100
                print(f"[{idx}/{total_tables}] ({progress:.1f}%) 正在处理表: {table_name}")

                # 2. 获取精简字段信息 (列名, 类型, 注释)
                # 使用 full_columns 获取更多元数据
                cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")
                columns = cursor.fetchall()

                # 加载字段描述信息
                field_descriptions = load_field_descriptions(table_name, database, table_db_mapping)
                if field_descriptions:
                    print(f"  已加载 {len(field_descriptions)} 个字段描述")

                # 构建新的格式：Columns 和 Example Value 分开
                column_descriptions = []  # 存储列描述
                example_values = {}  # 存储示例值，key为列名，value为值列表
                column_types = {}  # 存储字段类型信息

                # 获取索引信息，按 Key_name 分组
                index_info = {}  # {key_name: {"columns": [], "non_unique": bool}}
                try:
                    cursor.execute(f"SHOW INDEX FROM `{table_name}`")
                    indexes = cursor.fetchall()
                    for idx in indexes:
                        key_name = idx.get('Key_name', '')
                        column_name = idx.get('Column_name', '')
                        non_unique = bool(idx.get('Non_unique', 1))

                        if key_name not in index_info:
                            index_info[key_name] = {
                                'columns': [],
                                'non_unique': non_unique
                            }
                        index_info[key_name]['columns'].append(column_name)
                except Exception as e:
                    print(f"  ⚠️ 获取索引信息失败: {e}")

                for col in columns:
                    field_name = col['Field']
                    field_name_lower = field_name.lower()

                    # 优先使用CSV中的data_format，如果没有则使用数据库中的Type
                    field_type = col['Type']
                    if field_name_lower in field_descriptions:
                        _, data_format = field_descriptions[field_name_lower]
                        if data_format:
                            field_type = data_format

                    # 保存字段类型信息（保留原始类型，不使用data_format覆盖）
                    original_type = col['Type']
                    column_types[field_name] = original_type

                    key_info = "PRIMARY KEY" if col['Key'] == 'PRI' else ""

                    # 构建字段描述：只包含注释（不包含类型和主键信息）
                    description_parts = []

                    # 添加数据库注释
                    if col['Comment']:
                        description_parts.append(col['Comment'])

                    # 添加CSV中的字段描述
                    if field_name_lower in field_descriptions:
                        column_description, _ = field_descriptions[field_name_lower]
                        if column_description:
                            description_parts.append(column_description)

                    # 组合描述（如果没有注释，使用空字符串）
                    description = " | ".join(description_parts) if description_parts else ""
                    if description:
                        column_descriptions.append(f"- {field_name}: {description}")
                    else:
                        column_descriptions.append(f"- {field_name}")

                    # 对于非ID结尾的字段，进行随机采样
                    # 判断是否为ID字段：以id或_id结尾（忽略大小写）
                    field_lower = field_name.lower()
                    is_id_field = field_lower.endswith('id') or field_lower.endswith('_id')
                    sample_items = []
                    if not is_id_field:
                        try:
                            # 随机采样3个不同的非NULL值
                            cursor.execute(
                                f"SELECT DISTINCT `{field_name}` FROM `{table_name}` "
                                f"WHERE `{field_name}` IS NOT NULL "
                                f"ORDER BY RAND() LIMIT 3"
                            )
                            samples = cursor.fetchall()
                            if samples:
                                for row in samples:
                                    if row[field_name] is not None:
                                        original_value = row[field_name]

                                        # 将所有值转为字符串判断长度
                                        value_str = str(original_value)

                                        # 如果字符串长度超过50个字符，截断
                                        if len(value_str) > 50:
                                            value_str = value_str[:47] + "..."

                                        # 保存截断后的字符串值（按原值存储）
                                        sample_items.append(value_str)
                        except Exception:
                            # 如果采样失败（如字段不存在或查询错误），忽略
                            pass

                    # 如果有采样值，添加到示例值字典
                    if sample_items:
                        # 用 | 分割，无需引号包裹
                        sample_json = ' | '.join(sample_items)
                        example_values[field_name] = sample_json

                # 组合成新的格式
                lines = [f"Table: {table_name}", "Columns:"]
                lines.extend(column_descriptions)

                # 如果有示例值，添加 Example Value 部分
                if example_values:
                    lines.append("Example Values:")
                    for field_name, sample_json in example_values.items():
                        lines.append(f"- {field_name}: {sample_json}")

                final_text = "\n".join(lines)

                rag_contents.append(final_text)

                # 创建该表的SchemaMetadata
                table_meta = SchemaMetadata(
                    table_name=table_name.lower(),
                    database=database,
                    column_types=column_types,
                    indexes=index_info
                )
                table_metas.append(table_meta)

        # 写入纯文本文件，每个 DDL 之间用一个换行符隔断
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(rag_contents))

        print(f"✅ RAG 格式 Schema 已导出: {output_file}")

        return rag_contents, table_metas

    except pymysql.err.OperationalError as e:
        error_code, error_msg = e.args
        if error_code == 2003:
            print(f"❌ 无法连接到 MySQL 服务器: {host}:{port}")
            print("   请检查:")
            print("   1. MySQL 服务是否正在运行")
            print("   2. 主机地址和端口是否正确")
            print("   3. 防火墙是否允许连接")
            print(f"   错误详情: {error_msg}")
        else:
            print(f"❌ MySQL 操作错误 ({error_code}): {error_msg}")
        raise
    except pymysql.err.Error as e:
        print(f"❌ MySQL 错误: {e}")
        raise
    finally:
        if 'connection' in locals():
            connection.close()

def embed_and_store_to_milvus(
    ddls: list[str],
    table_metas: list[SchemaMetadata] = None,
    collection_name: str = "bird",
    database: str = "bird",
    batch_size: int = 32,
    mock: bool = False
) -> None:
    """
    将DDL列表进行embedding并存储到Milvus

    Args:
        ddls: DDL文本列表
        table_metas: SchemaMetadata列表，包含每个表的元数据（column_types, indexes）
        collection_name: Milvus collection名称，默认为"bird"
        database: 数据库名称，用于metadata
        batch_size: 批量处理大小，默认为32
        mock: 是否使用mock模式（只打印不存储），默认为False
    """
    if table_metas is None:
        table_metas = []
    if not ddls:
        print("⚠️  DDL列表为空，跳过embedding和存储")
        return

    mode_str = "Mock模式（仅打印）" if mock else "真实存储"
    print(f"\n开始将 {len(ddls)} 个DDL进行embedding并存储到Milvus... [{mode_str}]")

    # 初始化BGE embedder
    embedder = BGEEmbedder()

    # 只在非mock模式下初始化Milvus wrapper
    if not mock:
        # BGE-M3的稠密向量维度是1024
        # 先检查 collection 是否存在，如果存在则删除
        temp_milvus = MilvusWrapper(
            collection_name=collection_name,
            dimension=1024,
            auto_create=False  # 不自动创建，只用于检查
        )

        if temp_milvus.collection_exists():
            print(f"⚠️  Collection '{collection_name}' 已存在，正在删除...")
            temp_milvus.drop_collection()
            print(f"✅ 已删除 Collection '{collection_name}'")

        # 创建新的 collection
        print(f"📦 正在创建 Collection '{collection_name}'...")
        milvus = MilvusWrapper(
            collection_name=collection_name,
            dimension=1024,
            auto_create=True  # 自动创建新的 collection
        )
        print(f"✅ Collection '{collection_name}' 创建成功")

    total_ddls = len(ddls)

    # 批量处理，每次处理一批（避免内存过大）
    for batch_start in range(0, total_ddls, batch_size):
        batch_end = min(batch_start + batch_size, total_ddls)
        batch_ddls = ddls[batch_start:batch_end]
        batch_num = batch_start // batch_size + 1
        total_batches = (total_ddls + batch_size - 1) // batch_size

        print(f"[批次 {batch_num}/{total_batches}] 正在处理 DDL {batch_start+1}-{batch_end}/{total_ddls}")

        # 获取稠密向量和稀疏向量
        dense_vectors = embedder.embed_texts_dense(batch_ddls)
        sparse_vectors = embedder.embed_texts_sparse(batch_ddls)

        # 提取表名并生成ID和metadata
        ids = []
        metadatas = []
        for i, ddl_text in enumerate(batch_ddls):
            # 从DDL文本中提取表名（第一行的"Table: xxx"）
            table_name = "unknown"
            if ddl_text.startswith("Table: "):
                table_name = ddl_text.split("\n")[0].replace("Table: ", "").strip().lower()

            # 使用UUID生成唯一ID
            ids.append(str(uuid.uuid4()))

            # 查找对应的metadata（从table_metas中按表名匹配）
            meta = None
            for tm in table_metas:
                if tm.table_name == table_name:
                    meta = tm
                    break

            if meta is not None:
                # 使用已有的metadata，保留column_types和indexes
                metadatas.append(meta)
            else:
                # 如果没有找到，创建新的metadata
                metadatas.append(SchemaMetadata(
                    table_name=table_name,
                    database=database
                ))

        if mock:
            # Mock模式：打印每个DDL的详细信息
            for i in range(len(batch_ddls)):
                print(f"\n--- DDL {batch_start + i + 1}/{total_ddls} ---")
                print(f"ID: {ids[i]}")
                print(f"Metadata: {metadatas[i]}")
                print(f"DDL (前200字符): {batch_ddls[i][:200]}...")

                # 打印稠密向量前5个值
                dense_preview = dense_vectors[i][:5]
                print(f"稠密向量 (前5个值): {dense_preview} (总长度: {len(dense_vectors[i])})")

                # 打印稀疏向量前5个值（转换为列表）
                sparse_dict = sparse_vectors[i]
                sparse_items = list(sparse_dict.items())[:5]
                print(f"稀疏向量 (前5个值): {sparse_items} (总长度: {len(sparse_dict)})")
        else:
            # 真实存储到Milvus
            milvus.add(
                vectors=dense_vectors,
                sparse_vectors=sparse_vectors,
                documents=batch_ddls,
                metadatas=metadatas,
                ids=ids
            )
            print(f"[批次 {batch_num}/{total_batches}] ✅ 已存储 {len(batch_ddls)} 个DDL到Milvus")

    if mock:
        print(f"\n✅ Mock模式完成，共处理 {total_ddls} 个DDL（未实际存储）")
    else:
        print(f"\n✅ 所有DDL已成功存储到Milvus collection '{collection_name}'，共 {total_ddls} 条")


def update_metadata_in_milvus(
    table_metas: list[SchemaMetadata],
    collection_name: str = "bird",
    mock: bool = False
) -> None:
    """
    只更新 Milvus 中的 metadata（不重新 embedding）

    Args:
        table_metas: SchemaMetadata列表，包含每个表的元数据（column_types, indexes）
        collection_name: Milvus collection名称，默认为"bird"
        mock: 是否使用mock模式（只打印不更新），默认为False
    """
    if not table_metas:
        print("⚠️  table_metas 为空，跳过 metadata 更新")
        return

    mode_str = "Mock模式（仅打印）" if mock else "真实更新"
    print(f"\n开始更新 Milvus 中 {len(table_metas)} 个表的 metadata... [{mode_str}]")

    milvus = MilvusWrapper(
        collection_name=collection_name,
        dimension=1024,
        auto_create=False
    )

    if not milvus.collection_exists():
        print(f"⚠️  Collection '{collection_name}' 不存在，请先运行完整流程")
        return

    updated = 0
    skipped = 0
    not_found = 0

    for meta in table_metas:
        table_name = meta.table_name
        print(f"  处理表: {table_name}")

        # 将 dataclass 转换为字典
        metadata_dict = {
            "table_name": meta.table_name,
            "database": meta.database,
            "type": meta.type,
            "column_types": meta.column_types,
            "indexes": meta.indexes
        }

        if mock:
            print(f"    [Mock] 将更新 metadata: column_types={len(meta.column_types)} 列, indexes={len(meta.indexes)} 个")
            skipped += 1
        else:
            # 先用 table_name 查找 ID
            record_id = milvus.get_id_by_metadata("table_name", table_name)
            if record_id is None:
                print("    ⚠️  未找到记录")
                not_found += 1
                continue

            # 用 ID 更新 metadata
            success = milvus.update_metadata(record_id, metadata_dict)
            if success:
                print(f"    ✅ 已更新 (ID: {record_id})")
                updated += 1
            else:
                skipped += 1

    print(f"\n✅ Metadata 更新完成: 成功 {updated}, 未找到 {not_found}, 跳过 {skipped}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="导出数据库Schema并存储到Milvus向量数据库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整流程：导出Schema、embedding并存储到Milvus
  python ddl_embed_md.py

  # 只更新metadata，不重新embedding
  python ddl_embed_md.py --only-update-metadata

  # Mock模式预览只更新metadata的效果
  python ddl_embed_md.py --only-update-metadata --mock

  # 指定数据库连接参数
  python ddl_embed_md.py --host localhost --port 3307 --user root --password 123 --database mydb
        """
    )
    parser.add_argument('--host', type=str, default='127.0.0.1', help='MySQL主机地址')
    parser.add_argument('--port', type=int, default=3306, help='MySQL端口')
    parser.add_argument('--user', type=str, default='root', help='MySQL用户名')
    parser.add_argument('--password', type=str, default='123', help='MySQL密码')
    parser.add_argument('--database', type=str, default='bird', help='数据库名')
    parser.add_argument('--output', type=str, default=None, help='输出文件路径')
    parser.add_argument('--collection', type=str, default='bird', help='Milvus collection名称')
    parser.add_argument('--batch-size', type=int, default=32, help='批量处理大小')
    parser.add_argument('--mock', action='store_true', help='Mock模式，只打印不实际存储')
    parser.add_argument('--only-update-metadata', action='store_true',
                        help='只更新Milvus中的metadata，不重新embedding（需要先运行完整流程）')

    args = parser.parse_args()

    data_dir = Path(__file__).parent / "output"
    output_file = args.output or (data_dir / "rag_schema.sql")

    if args.only_update_metadata:
        # 只更新metadata模式
        print("📋 模式：只更新 metadata")
        ddls, table_metas = export_schema_for_rag(
            host=args.host,
            user=args.user,
            password=args.password,
            database=args.database,
            output_file=output_file
        )
        update_metadata_in_milvus(
            table_metas=table_metas,
            collection_name=args.collection,
            mock=args.mock
        )
    else:
        # 完整流程模式
        print("📋 模式：完整流程（导出Schema + embedding + 存储到Milvus）")
        ddls, table_metas = export_schema_for_rag(
            host=args.host,
            user=args.user,
            password=args.password,
            database=args.database,
            output_file=output_file
        )
        embed_and_store_to_milvus(
            ddls=ddls,
            table_metas=table_metas,
            collection_name=args.collection,
            database=args.database,
            batch_size=args.batch_size,
            mock=args.mock
        )
