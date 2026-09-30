from adapters.openai_adapter import OpenAIAdapter
from adapters.crewai_adapter import CrewAIAdapter
from adapters.claude_code_adapter import ClaudeCodeAdapter
from adapters.lyzr_adapter import LyzrAdapter
from adapters.portable_adapter import PortableAdapter
from tools.registry import build_registry

def test_adapter_boundaries_delegate():
    portable = PortableAdapter(build_registry())
    adapters = [
        OpenAIAdapter(portable),
        CrewAIAdapter(portable),
        ClaudeCodeAdapter(portable),
        LyzrAdapter(portable),
    ]
    args = {
        "execution_time_ms": 100,
        "rows_examined": 100,
        "rows_returned": 10,
        "frequency_per_hour": 1,
    }
    for adapter in adapters:
        assert adapter.invoke("estimate-query-cost", args)["status"] == "ok"
