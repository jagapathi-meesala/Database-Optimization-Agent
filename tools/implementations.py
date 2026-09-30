from __future__ import annotations

def _number(data, key, minimum=0.0):
    value = data.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{key} must be numeric")
    if value < minimum:
        raise ValueError(f"{key} must be >= {minimum}")
    return float(value)

def _name(value, field):
    if not isinstance(value, str) or not value.strip() or not all(c.isalnum() or c in "_-" for c in value):
        raise ValueError(f"{field} must be a non-empty safe identifier")

def validate_query(data):
    _number(data, "execution_time_ms")
    _number(data, "rows_examined")
    _number(data, "rows_returned")
    _number(data, "frequency_per_hour")

def analyze_query(data):
    validate_query(data)
    execution = float(data["execution_time_ms"])
    examined = float(data["rows_examined"])
    returned = float(data["rows_returned"])
    frequency = float(data["frequency_per_hour"])
    ratio = None if returned == 0 else examined / returned
    signals = []
    if execution >= 500:
        signals.append("high_execution_time")
    if ratio is not None and ratio >= 100:
        signals.append("high_row_examination_ratio")
    if frequency >= 100:
        signals.append("high_frequency")
    return {
        "tool": "analyze-query",
        "status": "ok",
        "signals": signals,
        "evidence": {
            "execution_time_ms": execution,
            "rows_examined": examined,
            "rows_returned": returned,
            "frequency_per_hour": frequency,
            "row_examination_ratio": ratio,
        },
        "recommendation": "Investigate query plan and indexing evidence before changing the query."
        if signals else "No configured high-cost signal was detected in the supplied metrics.",
        "limitations": ["Thresholds are deterministic heuristics and are not benchmark results."]
    }

def validate_indexes(data):
    table = data.get("table")
    _name(table, "table")
    for field in ("filter_columns", "order_columns", "existing_indexes"):
        if not isinstance(data.get(field), list):
            raise ValueError(f"{field} must be a list")
    for col in data["filter_columns"] + data["order_columns"]:
        _name(col, "column")
    for idx in data["existing_indexes"]:
        if not isinstance(idx, list) or not idx:
            raise ValueError("existing_indexes must contain non-empty column lists")
        for col in idx:
            _name(col, "index column")

def recommend_indexes(data):
    validate_indexes(data)
    filters = list(dict.fromkeys(data["filter_columns"]))
    ordering = [c for c in data["order_columns"] if c not in filters]
    candidate = filters + ordering
    existing = {tuple(x) for x in data["existing_indexes"]}
    if not candidate:
        return {"tool": "recommend-indexes", "status": "ok", "candidates": [], "reason": "No filter or order columns supplied."}
    if tuple(candidate) in existing or any(tuple(candidate[:len(idx)]) == idx for idx in existing if len(idx) <= len(candidate)):
        candidates = []
        reason = "The deterministic candidate is already represented by an existing index prefix."
    else:
        candidates = [candidate]
        reason = "Candidate orders filter columns before ordering columns using the supplied workload metadata."
    return {
        "tool": "recommend-indexes",
        "status": "ok",
        "table": data["table"],
        "candidates": candidates,
        "reason": reason,
        "limitations": ["This is an index candidate, not a command to create the index.", "Selectivity, write amplification, and storage statistics were not supplied."]
    }

def validate_schema(data):
    tables = data.get("tables")
    if not isinstance(tables, list) or not tables:
        raise ValueError("tables must be a non-empty list")
    for table in tables:
        if not isinstance(table, dict):
            raise ValueError("each table must be an object")
        _name(table.get("name"), "table name")
        if not isinstance(table.get("columns"), list) or not table["columns"]:
            raise ValueError("each table must have a non-empty columns list")

def analyze_schema(data):
    validate_schema(data)
    findings = []
    for table in data["tables"]:
        cols = table["columns"]
        names = [c.get("name") for c in cols]
        if any(not isinstance(n, str) or not n.strip() for n in names):
            raise ValueError("column names must be non-empty strings")
        duplicates = sorted({n for n in names if names.count(n) > 1})
        if duplicates:
            findings.append({"table": table["name"], "type": "duplicate_column_names", "columns": duplicates})
        if not table.get("primary_key"):
            findings.append({"table": table["name"], "type": "missing_primary_key_metadata"})
        nullable = sum(1 for c in cols if c.get("nullable") is True)
        if cols and nullable / len(cols) > 0.75:
            findings.append({"table": table["name"], "type": "high_nullable_column_fraction", "fraction": nullable / len(cols)})
    return {
        "tool": "analyze-schema",
        "status": "ok",
        "findings": findings,
        "limitations": ["Schema analysis uses metadata only and does not inspect live constraints or statistics."]
    }

def validate_cost(data):
    for key in ("execution_time_ms", "rows_examined", "rows_returned", "frequency_per_hour"):
        _number(data, key)

def estimate_query_cost(data):
    validate_cost(data)
    cost = float(data["execution_time_ms"]) * float(data["frequency_per_hour"])
    returned = float(data["rows_returned"])
    ratio = None if returned == 0 else float(data["rows_examined"]) / returned
    return {
        "tool": "estimate-query-cost",
        "status": "ok",
        "estimate": {
            "workload_cost_ms_per_hour": cost,
            "row_examination_ratio": ratio,
            "formula": "execution_time_ms * frequency_per_hour"
        },
        "limitations": ["Estimate uses supplied metrics and does not measure database CPU, I/O, locks, cache behavior, or concurrency."]
    }
