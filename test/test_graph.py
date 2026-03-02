from graph import DataHuntGraph


def test_datahunt_graph_run_once(capsys):
    graph = DataHuntGraph()
    app = graph._graph  # compiled graph
    initial_state = {
        "question": "测试问题",
        "rewritten_question": "",
        "matched_question": None,
        "generated_sql": None,
        "DDL": [],
        "relevant_docs": [],
        "exec_result": None,
        "exec_error": None,
        "answer": "",
    }
    result = app.invoke(initial_state)
    assert result["answer"].startswith("执行结果")

