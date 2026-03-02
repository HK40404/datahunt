pytest test/test_openai.py -vs

pytest test/test_tool_manager.py::test_llm_no_suitable_tool -vs
pytest test/test_config.py::test_config_attribute_access -vs
pytest test/test_table_relation_provider.py::test_manual -vs

pytest test/test_openai.py -m manual -vs

# benchmark
python src/pipeline/rag_benchmark.py --evidence --rag-augmented --top-k 1 3 5 10 12
python src/pipeline/langgraph_benchmark.py --exec-accuracy --concurrency 10

# 打印图结构
# from graph.graph import datahunt_graph
# print(datahunt_graph._graph.get_graph().draw_mermaid())