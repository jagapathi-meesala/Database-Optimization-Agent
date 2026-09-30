---
name: index-analysis
description: Generate deterministic index candidates from supplied query filter, ordering, and existing-index metadata.
---

# Index Analysis

## Inputs
Table identifier, filter columns, ordering columns, and existing indexes.

## Behavior
Place filter columns before ordering columns and avoid recommending a candidate already represented by an existing index prefix.

## Outputs
Candidate index definitions and explicit limitations.

## Invalid Inputs
Reject malformed identifiers and malformed index lists.
