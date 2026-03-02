import json
from pathlib import Path

import networkx as nx


class TableRelationProvider:
    """提供数据表关系的类，基于 NetworkX 无向图实现"""

    def __init__(self, json_path: str | Path | None = None):
        """
        初始化 TableRelationProvider

        Args:
            json_path: NetworkX JSON 文件路径，默认为项目中的 table_relationships.json
        """
        if json_path is None:
            # 默认使用项目中的 JSON 文件
            json_path = Path(__file__).parent.parent / "pipeline" / "output" / "table_relation" / "table_relationships.json"

        self.json_path = Path(json_path)
        self.graph = self._load_graph()

    def _load_graph(self) -> nx.Graph:
        """
        从 JSON 文件加载无向图

        Returns:
            NetworkX 无向图对象
        """
        with open(self.json_path, encoding='utf-8') as f:
            data = json.load(f)

        # 使用 node_link_data 格式创建图
        graph = nx.node_link_graph(data)

        return graph

    def get_connected_tables(
        self,
        table_names: list[str],
        max_hops: int | None = None,
        total_limit: int | None = None,
        single_limit: int | None = None
    ) -> list[str]:
        """
        获取与指定表名列表相关联的表

        Args:
            table_names: 输入的表名列表
            max_hops: 最大跳数，如果为 None 则获取所有在同一连通分量中的表
            total_limit: 限制返回的关联表总数量，None 表示不限制
            single_limit: 单个表最多返回的关联表数量，None 表示不限制

        Returns:
            与输入表中任何一个表相关联的表名的列表（不包括输入表本身），按加入顺序返回

        Raises:
            ValueError: 如果任何一个表名不在图中
        """
        if not table_names:
            return []

        # 验证所有表名都在图中
        missing_tables = [name for name in table_names if name not in self.graph]
        if missing_tables:
            raise ValueError(f"以下表不在关系图中: {missing_tables}")

        # 验证参数
        if total_limit is not None and total_limit <= 0:
            raise ValueError("total_limit 必须大于 0")
        if single_limit is not None and single_limit <= 0:
            raise ValueError("single_limit 必须大于 0")

        # 如果未指定跳数，返回所有连通分量中的表
        if max_hops is None:
            result: list[str] = []
            added_tables: set = set()  # 用于快速判断重复
            for table_name in table_names:
                connected_component = nx.node_connected_component(self.graph, table_name)
                for table in connected_component:
                    if table not in table_names and table not in added_tables:
                        result.append(table)
                        added_tables.add(table)
                # 检查是否达到 total_limit
                if total_limit is not None and len(result) >= total_limit:
                    break
            # 应用 total_limit
            if total_limit is not None:
                return result[:total_limit]
            return result

        # 如果指定了跳数
        if max_hops < 0:
            raise ValueError("跳数必须大于等于 0")

        # 收集每个输入表的所有关联表及其跳数
        all_related: dict[str, dict[int, list[str]]] = {}  # {表名: {跳数: [表名列表]}}
        for table_name in table_names:
            path_lengths = nx.single_source_shortest_path_length(self.graph, table_name, cutoff=max_hops)
            # 按跳数分组
            hops_dict: dict[int, list[str]] = {}
            for node, length in path_lengths.items():
                if length > 0 and node not in table_names:
                    if length not in hops_dict:
                        hops_dict[length] = []
                    hops_dict[length].append(node)
            # 每个跳数层内按表名字母排序
            for length in hops_dict:
                hops_dict[length].sort()
            all_related[table_name] = hops_dict

        # 按跳数分层收集：先1跳，再2跳...
        result: list[str] = []
        added_tables: set = set()  # 用于快速判断重复
        # 记录每个源表已添加的表数，用于 single_limit 控制
        source_added_count: dict[str, int] = {t: 0 for t in table_names}

        for hop in range(1, max_hops + 1):
            for table_name in table_names:
                # 检查 total_limit
                if total_limit is not None and len(result) >= total_limit:
                    break

                # 检查 single_limit（单个源表在所有跳数内最多添加 single_limit 个）
                if single_limit is not None and source_added_count[table_name] >= single_limit:
                    continue

                hop_tables = all_related[table_name].get(hop, [])
                # 计算该源表在该跳数层还能添加多少个
                remaining = single_limit - source_added_count[table_name] if single_limit is not None else len(hop_tables)
                for node in hop_tables[:remaining]:
                    if node not in added_tables:
                        result.append(node)
                        added_tables.add(node)
                        source_added_count[table_name] += 1
                        # 检查 total_limit
                        if total_limit is not None and len(result) >= total_limit:
                            break

            # 检查 total_limit
            if total_limit is not None and len(result) >= total_limit:
                break

        return result

    def has_table(self, table_name: str) -> bool:
        """
        检查表是否存在于关系图中

        Args:
            table_name: 表名

        Returns:
            如果表存在返回 True，否则返回 False
        """
        return table_name in self.graph
