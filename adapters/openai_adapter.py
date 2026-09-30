class OpenAIAdapter:
    """Compatibility boundary for OpenAI-style tool invocation.

    No OpenAI SDK dependency is required by the core. Integration is not claimed
    as tested until the SDK is installed and exercised.
    """
    def __init__(self, portable_adapter):
        self.portable_adapter = portable_adapter

    def invoke(self, tool_name, arguments):
        return self.portable_adapter.invoke(tool_name, arguments)
