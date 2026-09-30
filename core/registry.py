from contracts.tool_contract import ToolContract

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolContract] = {}

    def register(self, tool: ToolContract) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def discover(self) -> list[str]:
        return sorted(self._tools)

    def execute(self, name: str, inputs: dict) -> dict:
        tool = self._tools.get(name)
        if tool is None:
            return {"tool": name, "status": "error", "error": "unknown_tool"}
        try:
            tool.validate(inputs)
            return tool.execute(inputs)
        except ValueError as exc:
            return {"tool": name, "status": "error", "error": "validation_error", "message": str(exc)}
        except Exception as exc:
            return {"tool": name, "status": "error", "error": "execution_error", "message": str(exc)}
