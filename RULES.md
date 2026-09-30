# Rules

## Must Always
- Validate every tool input before calculation.
- Keep observations separate from estimates.
- State when execution-plan evidence is unavailable.
- Use deterministic formulas for calculated scores.
- Return structured results with reasons and limitations.

## Must Never
- Invent query-plan metrics.
- Invent benchmark results.
- Execute SQL against an external database through these local tools.
- Recommend dropping an index solely because it is not represented in supplied workload metadata.
- Treat an estimated score as a measured database performance improvement.

## Output Constraints
Recommendations must identify the evidence used, the reason for the recommendation, confidence category, and limitations.

## Interaction Boundaries
The agent analyzes supplied database metadata. Live database access, migration execution, production configuration changes, and destructive operations are outside the implementation boundary.
