"""
TableRelationProvider 测试程序 - 使用真实数据
"""
import pytest

from context.table_relation_provider import TableRelationProvider


@pytest.fixture
def provider():
    """创建 TableRelationProvider 实例，使用真实数据"""
    return TableRelationProvider()


def test_init_with_default_path(provider):
    """测试使用默认路径初始化"""
    assert provider.graph is not None
    assert len(provider.graph.nodes) > 0
    assert len(provider.graph.edges) > 0


def test_init_file_not_found():
    """测试文件不存在时的异常处理"""
    with pytest.raises(FileNotFoundError):
        TableRelationProvider(json_path="nonexistent_file.json")


def test_has_table_exists(provider):
    """测试检查存在的表 - 真实数据"""
    real_tables = ["account", "schools", "atom", "member", "posts", "cards",
                   "disp", "client", "satscores", "molecule", "income"]
    for table in real_tables:
        assert provider.has_table(table), f"表 {table} 应该存在"


def test_has_table_not_exists(provider):
    """测试检查不存在的表"""
    assert provider.has_table("nonexistent_table_xyz_123") is False


def test_get_connected_tables_income_max_hops_1(provider):
    """测试获取 income 表的直接关联表（使用 get_connected_tables max_hops=1）- 真实数据"""
    related = provider.get_connected_tables(["income"], max_hops=1)

    assert isinstance(related, list)
    assert len(related) == 1
    assert "income" not in related
    assert "member" in related


def test_get_connected_tables_not_exists(provider):
    """测试获取关联表 - 表不存在"""
    with pytest.raises(ValueError, match="以下表不在关系图中"):
        provider.get_connected_tables(["nonexistent_table"], max_hops=1)


def test_get_connected_tables_income_without_hops(provider):
    """测试获取 income 表的连通分量（不指定跳数）- 真实数据"""
    connected = provider.get_connected_tables(["income"])

    assert isinstance(connected, list)
    assert len(connected) == 7
    assert "income" not in connected
    # 验证包含所有连通分量中的表
    expected_tables = ["budget", "zip_code", "member", "major", "expense", "event", "attendance"]
    assert set(connected) == set(expected_tables)


def test_get_connected_tables_income_with_hops(provider):
    """测试 income 表的跳数限制功能 - 真实数据"""
    # 验证 income 表存在
    assert provider.has_table("income"), "income 表应该存在"

    # 测试 max_hops=0（应该返回空列表）
    connected_0 = provider.get_connected_tables(["income"], max_hops=0)
    assert isinstance(connected_0, list)
    assert len(connected_0) == 0

    # 测试 max_hops=1（直接关联）
    connected_1 = provider.get_connected_tables(["income"], max_hops=1)
    assert isinstance(connected_1, list)
    assert len(connected_1) == 1
    assert "member" in connected_1
    assert "income" not in connected_1

    # 测试 max_hops=2（应该包含所有连通分量）
    connected_2 = provider.get_connected_tables(["income"], max_hops=2)
    assert isinstance(connected_2, list)
    assert len(connected_2) == 7
    assert "member" in connected_2
    assert "income" not in connected_2
    # 验证包含所有连通分量中的表
    expected_tables = {"budget", "zip_code", "member", "major", "expense", "event", "attendance"}
    assert set(connected_2) == expected_tables

    # 测试不指定 max_hops（应该返回所有连通分量）
    connected_all = provider.get_connected_tables(["income"])
    assert isinstance(connected_all, list)
    assert len(connected_all) == 7
    assert set(connected_all) == expected_tables
    assert set(connected_all) == set(connected_2)  # 应该等于 max_hops=2 的结果


def test_get_connected_tables_income_hops_comparison(provider):
    """测试 income 表不同跳数的结果比较 - 真实数据"""
    # 验证跳数递增时结果也递增
    connected_0 = provider.get_connected_tables(["income"], max_hops=0)
    connected_1 = provider.get_connected_tables(["income"], max_hops=1)
    connected_2 = provider.get_connected_tables(["income"], max_hops=2)
    connected_all = provider.get_connected_tables(["income"])

    # 验证包含关系：0跳 ⊆ 1跳 ⊆ 2跳 ⊆ 所有连通分量
    assert set(connected_0).issubset(set(connected_1))
    assert set(connected_1).issubset(set(connected_2))
    assert set(connected_2).issubset(set(connected_all))

    # 验证大小递增
    assert len(connected_0) < len(connected_1)
    assert len(connected_1) < len(connected_2)
    assert len(connected_2) == len(connected_all)  # 2跳已经包含所有连通分量


def test_get_connected_tables_income_invalid_hops(provider):
    """测试 income 表的无效跳数参数 - 真实数据"""
    # 测试负数跳数
    with pytest.raises(ValueError, match="跳数必须大于等于 0"):
        provider.get_connected_tables(["income"], max_hops=-1)

    # 测试不存在的表
    with pytest.raises(ValueError, match="以下表不在关系图中"):
        provider.get_connected_tables(["nonexistent_table"], max_hops=1)


def test_get_connected_tables_income_hops_1_vs_all(provider):
    """测试 income 表的 1跳关联与连通分量的区别 - 真实数据"""
    related = provider.get_connected_tables(["income"], max_hops=1)
    connected = provider.get_connected_tables(["income"])

    # 连通分量应该包含 1跳关联的表
    assert set(related).issubset(set(connected))
    # 连通分量应该更多（包含间接关联）
    assert len(connected) > len(related)
    # 验证间接关联的表
    assert "budget" in connected
    assert "event" in connected
    assert "budget" not in related
    assert "event" not in related


def test_return_type_list(provider):
    """测试返回类型为 List - 使用 income 表"""
    result = provider.get_connected_tables(["income"], max_hops=1)
    assert isinstance(result, list)
    assert isinstance(provider.get_connected_tables(["income"]), list)
    assert isinstance(provider.get_connected_tables(["income"], max_hops=2), list)
    assert isinstance(provider.has_table("income"), bool)


def test_income_not_in_results(provider):
    """测试结果中不包含输入表本身 - 使用 income 表"""
    connected_1 = provider.get_connected_tables(["income"], max_hops=1)
    connected = provider.get_connected_tables(["income"])
    connected_2 = provider.get_connected_tables(["income"], max_hops=2)

    assert "income" not in connected_1
    assert "income" not in connected
    assert "income" not in connected_2


def test_symmetric_relationships_income(provider):
    """测试关系的对称性 - 使用 income 表"""
    # 如果 income 关联 member，那么 member 也应该关联 income
    income_related = provider.get_connected_tables(["income"], max_hops=1)
    member_related = provider.get_connected_tables(["member"], max_hops=1)

    assert "member" in income_related
    assert "income" in member_related


def test_get_connected_tables_empty_list(provider):
    """测试空列表输入"""
    result = provider.get_connected_tables([])
    assert isinstance(result, list)
    assert len(result) == 0


def test_get_connected_tables_one_missing(provider):
    """测试多个表名中有一个不存在的情况"""
    with pytest.raises(ValueError, match="以下表不在关系图中"):
        provider.get_connected_tables(["income", "nonexistent_table"], max_hops=1)


def test_get_connected_tables_total_limit(provider):
    """测试 total_limit 参数限制返回总数"""
    # income 的连通分量有7个表
    connected_all = provider.get_connected_tables(["income"])
    assert len(connected_all) == 7

    # 使用 total_limit=3 限制返回3个
    connected_limited = provider.get_connected_tables(["income"], total_limit=3)
    assert isinstance(connected_limited, list)
    assert len(connected_limited) == 3
    # 结果应该是前3个（按跳数分层顺序）
    assert connected_limited[:3] == connected_all[:3]


def test_get_connected_tables_single_limit(provider):
    """测试 single_limit 参数限制单个源表的关联表数量"""
    # 使用 member 和 income（它们共享一些关联表）
    # single_limit=1 意味着每个源表最多贡献1个表
    result = provider.get_connected_tables(["income", "member"], max_hops=2, single_limit=1)

    # 由于 income 和 member 1跳都指向对方，但会跳过输入表
    # 2跳时每个最多贡献1个
    assert isinstance(result, list)
    # 验证每个源表贡献的表数不超过 single_limit
    # 这里需要检查逻辑：结果中每个源表的关联表应该 <= 1


def test_get_connected_tables_order_by_hops(provider):
    """测试返回结果按跳数分层排序"""
    # 使用一个有多跳关联的表
    result = provider.get_connected_tables(["income"], max_hops=2)

    assert isinstance(result, list)
    # 1跳表应该在2跳表前面
    if "member" in result and len(result) > 1:
        member_idx = result.index("member")
        # member 是1跳表，应该在所有2跳表之前
        for i, table in enumerate(result):
            if table != "member" and table not in ["income"]:
                # 检查1跳表是否在2跳表前面
                assert member_idx < i, f"1跳表 member(索引{member_idx})应该在2跳表{table}(索引{i})前面"


def test_get_connected_tables_order_multiple_sources(provider):
    """测试多个源表时按源表顺序添加"""
    # 使用 income 和 member 作为源表
    result = provider.get_connected_tables(["income", "member"], max_hops=2)

    assert isinstance(result, list)
    # 验证返回类型
    assert "income" not in result
    assert "member" not in result


def test_get_connected_tables_total_limit_smaller_than_hops(provider):
    """测试 total_limit 比可能返回的表数小"""
    result = provider.get_connected_tables(["income"], total_limit=2, max_hops=2)

    assert isinstance(result, list)
    assert len(result) == 2
    # 应该是按跳数分层的前2个


def test_get_connected_tables_total_limit_invalid(provider):
    """测试 total_limit 无效值"""
    with pytest.raises(ValueError, match="total_limit 必须大于 0"):
        provider.get_connected_tables(["income"], total_limit=0)

    with pytest.raises(ValueError, match="total_limit 必须大于 0"):
        provider.get_connected_tables(["income"], total_limit=-1)


def test_get_connected_tables_single_limit_invalid(provider):
    """测试 single_limit 无效值"""
    with pytest.raises(ValueError, match="single_limit 必须大于 0"):
        provider.get_connected_tables(["income"], single_limit=0)

    with pytest.raises(ValueError, match="single_limit 必须大于 0"):
        provider.get_connected_tables(["income"], single_limit=-1)


def test_get_connected_tables_no_duplicate_tables(provider):
    """测试结果中没有重复的表"""
    # 使用有共同关联表的两个源表
    result = provider.get_connected_tables(["income", "member"], max_hops=2)

    assert isinstance(result, list)
    # 检查是否有重复
    assert len(result) == len(set(result)), "结果中不应该有重复的表"
