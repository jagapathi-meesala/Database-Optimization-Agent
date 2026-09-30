# Database Optimization Agent

A framework-independent OpenGAP agent for deterministic database performance analysis.

## Capabilities
- Query metadata analysis
- Index candidate analysis
- Schema risk analysis
- Relative query-cost estimation
- Explainable optimization recommendations

## Safety Boundary
The project does not connect to or modify a live database. It analyzes supplied metadata only.

## Repository
- `agent.yaml` — OpenGAP manifest
- `skills/` — declared skills
- `tools/` — tool contracts and implementations
- `core/` — framework-independent contracts and registry
- `adapters/` — portability boundaries
- `verification/` — structural checks
- `tests/` — pytest suite

## Validation
Run:

```bash
pytest -q
```

If the OpenGAP CLI is installed, additionally run:

```bash
opengap validate
```

The local test suite does not substitute for official OpenGAP CLI validation.
