import os

class ConfigurationError(RuntimeError):
    pass

def get_required(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ConfigurationError(f"Required environment variable is missing: {name}")
    return value
