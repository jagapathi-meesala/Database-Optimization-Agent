# Explainability

## Inputs and Data Sources
The agent accepts structured database metadata supplied by the caller, including query text metadata, execution metrics, index metadata, schema metadata, and simplified plan observations. The implementation does not fetch external database statistics, so all decisions are based only on the supplied inputs.

## Decision and Reasoning
The agent validates inputs and applies deterministic rules to identify high-cost query signals, index opportunities, and schema risks. Calculated estimates use documented formulas and are explicitly labeled as estimates rather than measured production improvements.

## Limits and Constraints
The agent does not connect to a database, execute SQL, change indexes, or modify configuration. Recommendations can be incomplete when execution plans, table statistics, workload frequency, or representative benchmark data are missing.

## Agent Purpose
The purpose is to convert structured database workload evidence into transparent optimization suggestions without performing database mutations.

## Input Mechanisms
Inputs are passed directly to framework-independent tool contracts. Each tool validates types, required fields, ranges, and collection sizes before execution.

## Decision Mechanisms
Query analysis checks supplied execution metrics and plan signals. Index analysis considers equality/filter columns, ordering columns, existing indexes, and workload frequency; schema analysis checks primary-key presence, nullable columns, duplicate column definitions, and basic normalization signals.

## Execution Limits
The tools operate only on in-memory input objects. No network connection, database driver, shell command, or migration runner is required by the core implementation.

## Output Contract
Every tool returns a structured result containing the tool name, status, findings or recommendation data, and limitations where applicable.

## Complete Execution Lifecycle
1. Receive structured input.
2. Validate the input against the tool contract.
3. Execute deterministic domain logic.
4. Produce structured findings.
5. Attach evidence and limitations.
6. Return the result without mutating external state.

## Tool-by-tool Behavior

### Analyze Query
Receives query metadata such as execution time, rows examined, rows returned, frequency, and plan flags. It calculates a relative cost score from supplied metrics and identifies the dominant signals.

### Recommend Indexes
Receives table columns, workload predicates/order columns, existing indexes, and query frequency. It identifies candidate composite indexes using deterministic column-order rules and excludes columns already covered by an existing suitable index.

### Analyze Schema
Receives table and column metadata. It identifies missing primary-key metadata, suspicious duplicate column names, excessive nullable columns, and very wide declared text fields.

### Estimate Query Cost
Receives execution time, rows examined, rows returned, and frequency. It computes a deterministic workload cost estimate using `execution_time_ms × frequency_per_hour` and reports the supplied row-examination ratio separately.

## Tool Inputs
All tool inputs are JSON-compatible dictionaries. Detailed schemas are stored in `tools/*.yaml`.

## Tool Validation
Invalid types, negative numeric values, empty required collections, and malformed identifiers are rejected with structured validation errors.

## Tool Failure Behavior
A tool returns a controlled error result rather than silently fabricating output. Unexpected implementation errors are converted to safe structured failures at the registry boundary.

## Deterministic Rules
The rules are documented in `RULES.md` and implemented in `tools/implementations.py`. No random values or model-generated benchmark claims are used.

## Formulas
Relative workload cost is `execution_time_ms × frequency_per_hour`. Row examination ratio is `rows_examined / rows_returned` when returned rows are greater than zero; otherwise the ratio is reported as unavailable.

## Worked Example
For a query taking 250 ms and running 120 times per hour, the deterministic workload cost estimate is 30,000 ms per hour. This is an estimate from supplied metadata, not a measured production saving.

## Explainability of Calculated Results
Every calculated result exposes the input values used for the calculation and the formula name. The agent does not convert the estimate into a claim that a proposed optimization will definitely improve latency.

## Provenance
The provenance of a result is the caller-provided input object and the deterministic implementation version represented by the repository commit. External database statistics are not implicitly consulted.
