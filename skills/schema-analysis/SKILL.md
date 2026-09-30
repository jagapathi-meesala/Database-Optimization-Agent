---
name: schema-analysis
description: Analyze supplied schema metadata for deterministic performance-related risks.
---

# Schema Analysis

## Inputs
Table names, column metadata, and primary-key metadata.

## Behavior
Check duplicate column names, missing primary-key metadata, and high nullable-column fractions.

## Outputs
Structured findings with limitations.

## Invalid Inputs
Reject empty tables, malformed table names, and invalid column collections.
