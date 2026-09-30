from contracts.tool_contract import ToolContract
from core.registry import ToolRegistry
from tools.implementations import (
    validate_query, analyze_query, validate_indexes, recommend_indexes,
    validate_schema, analyze_schema, validate_cost, estimate_query_cost,
)

def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ToolContract(
        "analyze-query", "Analyze supplied query workload metrics.",
        {"type": "object"}, {"type": "object"}, validate_query, analyze_query))
    registry.register(ToolContract(
        "recommend-indexes", "Generate deterministic index candidates from supplied workload metadata.",
        {"type": "object"}, {"type": "object"}, validate_indexes, recommend_indexes))
    registry.register(ToolContract(
        "analyze-schema", "Analyze supplied schema metadata for performance-related signals.",
        {"type": "object"}, {"type": "object"}, validate_schema, analyze_schema))
    registry.register(ToolContract(
        "estimate-query-cost", "Estimate hourly query workload cost from supplied metrics.",
        {"type": "object"}, {"type": "object"}, validate_cost, estimate_query_cost))
    return registry
