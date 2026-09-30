from tools.registry import build_registry

def test_registry_discovers_all_tools():
    registry = build_registry()
    assert registry.discover() == [
        "analyze-query",
        "analyze-schema",
        "estimate-query-cost",
        "recommend-indexes",
    ]

def test_query_analysis():
    result = build_registry().execute("analyze-query", {
        "execution_time_ms": 800,
        "rows_examined": 10000,
        "rows_returned": 50,
        "frequency_per_hour": 120,
    })
    assert result["status"] == "ok"
    assert "high_execution_time" in result["signals"]
    assert "high_row_examination_ratio" in result["signals"]

def test_query_validation():
    result = build_registry().execute("analyze-query", {
        "execution_time_ms": -1,
        "rows_examined": 10,
        "rows_returned": 1,
        "frequency_per_hour": 1,
    })
    assert result["status"] == "error"
    assert result["error"] == "validation_error"

def test_index_candidate():
    result = build_registry().execute("recommend-indexes", {
        "table": "orders",
        "filter_columns": ["customer_id"],
        "order_columns": ["created_at"],
        "existing_indexes": [],
    })
    assert result["status"] == "ok"
    assert result["candidates"] == [["customer_id", "created_at"]]

def test_existing_index_prefix_is_respected():
    result = build_registry().execute("recommend-indexes", {
        "table": "orders",
        "filter_columns": ["customer_id"],
        "order_columns": ["created_at"],
        "existing_indexes": [["customer_id"]],
    })
    assert result["candidates"] == []

def test_schema_analysis():
    result = build_registry().execute("analyze-schema", {
        "tables": [{
            "name": "orders",
            "primary_key": "id",
            "columns": [
                {"name": "id", "nullable": False},
                {"name": "customer_id", "nullable": True},
                {"name": "created_at", "nullable": True},
                {"name": "status", "nullable": True},
            ]
        }]
    })
    assert result["status"] == "ok"

def test_cost_formula():
    result = build_registry().execute("estimate-query-cost", {
        "execution_time_ms": 250,
        "rows_examined": 1000,
        "rows_returned": 10,
        "frequency_per_hour": 120,
    })
    assert result["estimate"]["workload_cost_ms_per_hour"] == 30000.0
    assert result["estimate"]["row_examination_ratio"] == 100.0

def test_unknown_tool():
    result = build_registry().execute("missing-tool", {})
    assert result["status"] == "error"
    assert result["error"] == "unknown_tool"

def test_adapter_boundary():
    from adapters.portable_adapter import PortableAdapter
    adapter = PortableAdapter(build_registry())
    result = adapter.invoke("estimate-query-cost", {
        "execution_time_ms": 100,
        "rows_examined": 100,
        "rows_returned": 10,
        "frequency_per_hour": 10,
    })
    assert result["status"] == "ok"
