"""
Summary 节点测试

测试 SummaryNode 的短结果和长结果模式
"""

import pytest
from graph.summary import SummaryNode


class TestSummaryNode:
    """SummaryNode 单元测试"""

    @pytest.fixture
    def summary_node(self):
        """创建 SummaryNode 实例"""
        return SummaryNode()

    # @pytest.mark.asyncio
    # async def test_short_result(self, summary_node):
    #     """测试短结果 (len <= 300)"""
    #     result = [
    #         {"team_long_name": "Manchester United"},
    #         {"team_long_name": "Liverpool FC"},
    #         {"team_long_name": "Chelsea FC"},
    #     ]

    #     answer = await summary_node.generate(
    #         question="球队名称？",
    #         generated_sql="SELECT team_long_name FROM Team",
    #         exec_result=result,
    #         validate_error=None,
    #         exec_error=""
    #     )

    #     # 短结果应该简洁
    #     assert "Manchester United" in answer or "Liverpool" in answer or "Chelsea" in answer

    @pytest.mark.asyncio
    async def test_long_result(self, summary_node):
        """测试长结果 (len > 300)"""
        result = """
        [
            {
                "team_long_name": "Manchester United Football Club",
                "league": "Premier League",
                "country": "England",
                "city": "Manchester",
                "stadium_name": "Old Trafford",
                "stadium_capacity": 74310,
                "founded_year": 1878,
                "nickname": "The Red Devils"
            },
            {
                "team_long_name": "Liverpool Football Club",
                "league": "Premier League",
                "country": "England",
                "city": "Liverpool",
                "stadium_name": "Anfield",
                "stadium_capacity": 61276,
                "founded_year": 1892,
                "nickname": "The Reds"
            },
            {
                "team_long_name": "Chelsea Football Club",
                "league": "Premier League",
                "country": "England",
                "city": "London",
                "stadium_name": "Stamford Bridge",
                "stadium_capacity": 40341,
                "founded_year": 1905,
                "nickname": "The Blues"
            },
            {
                "team_long_name": "Real Madrid Club de Fútbol",
                "league": "La Liga",
                "country": "Spain",
                "city": "Madrid",
                "stadium_name": "Santiago Bernabéu",
                "stadium_capacity": 83186,
                "founded_year": 1902,
                "nickname": "Los Blancos"
            },
            {
                "team_long_name": "Fußball-Club Bayern München e. V.",
                "league": "Bundesliga",
                "country": "Germany",
                "city": "Munich",
                "stadium_name": "Allianz Arena",
                "stadium_capacity": 75000,
                "founded_year": 1900,
                "nickname": "Die Bayern"
            },
            {
                "team_long_name": "Associazione Calcio Milan",
                "league": "Serie A",
                "country": "Italy",
                "city": "Milan",
                "stadium_name": "San Siro",
                "stadium_capacity": 75817,
                "founded_year": 189...
        """

        answer = await summary_node.generate(
            question="查询每个球队的详细信息",
            generated_sql="SELECT team_long_name, league, country, city, stadium_name, stadium_capacity, founded_year, nickname FROM Team",
            exec_result=result,
            validate_error=None,
            exec_error=""
        )

        print(answer)

        # 长结果应该包含详细解释
        assert len(answer) > 0
        assert "Manchester United" in answer or "查询结果" in answer or "球队" in answer
