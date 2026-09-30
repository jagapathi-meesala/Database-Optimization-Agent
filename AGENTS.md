# Agents

## Architecture
The agent is framework-independent. The core contract layer defines tool inputs and outputs, the registry discovers and executes tools, and adapters translate external framework calls into the same contract.

## Development Rules
Keep domain logic deterministic, validate inputs, avoid runtime configuration defaults, and preserve clear separation between analysis and execution.

## Tool Conventions
Every tool exposes a name, purpose, input schema, output expectations, validation behavior, and execution behavior.

## Testing Rules
Run `pytest -q` before claiming local test success. Documentation and manifest checks are part of the test suite.

## Portability
Framework adapters are compatibility boundaries only. A framework integration is not described as tested unless its package and adapter behavior have actually been exercised.
