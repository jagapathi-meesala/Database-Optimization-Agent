class CrewAIAdapter:
    """Compatibility boundary for CrewAI invocation."""
    def __init__(self, portable_adapter):
        self.portable_adapter = portable_adapter

    def invoke(self, tool_name, arguments):
        return self.portable_adapter.invoke(tool_name, arguments)
