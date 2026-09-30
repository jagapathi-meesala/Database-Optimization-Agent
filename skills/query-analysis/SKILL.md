---
name: query-analysis
description: Analyze supplied SQL workload metrics and explain deterministic performance signals.
---

# Query Analysis

## Inputs
Execution time, rows examined, rows returned, and query frequency.

## Behavior
Validate metrics, calculate the row-examination ratio when possible, identify configured high-cost signals, and return evidence with limitations.

## Outputs
Structured findings and a recommendation for further investigation.

## Invalid Inputs
Reject missing, non-numeric, or negative metrics.
