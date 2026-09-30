from core.registry import ToolRegistry

class PortableAdapter:
    """Framework-neutral invocation boundary."""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def invoke(self, tool_name: str, arguments: dict) -> dict:
        return self.registry.execute(tool_name, arguments)
