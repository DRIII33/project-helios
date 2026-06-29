# Project Helios Data Engine: Conformed Dimension Ledger

## Fact Matrix Table: `fact_candidate_pipeline`
This fact table captures every granular state transition an applicant undergoes throughout the recruitment cycle. It is pre-processed using window functions to evaluate state durations natively without complex self-joins.

| Column Name | Storage Type | Constraint | Definition |
| :--- | :--- | :--- | :--- |
| `pipeline_event_id` | STRING | PK | Unique system hash key isolating a specific transaction entry step. |
| `candidate_id` | STRING | FK | Unique key grouping an individual candidate's historical pipeline journey. |
| `requisition_id` | STRING | FK | Relational link mapping the applicant directly to an open headcount slot. |
| `source_channel` | STRING | Dimension | Ingestion-derived sourcing route. Missing attributes fallback to `SYSTEM_NULL_TRIGGER`. |
| `stage_reached` | STRING | Dimension | Pipeline milestone state string (`Applied`, `Phone Screen`, `Technical Interview`, etc.). |
| `stage_entry_time` | TIMESTAMP | Axis | The structured date and time execution mark when a candidate entered the state. |
| `recruiter_id` | STRING | FK | Key indicating the primary assigned owner managing the talent lifecycle. |
| `immediate_prior_stage`| STRING | Attribute | Captured via `LAG()` partitioning. Identifies the previous phase position. |
| `days_spent_in_prior_stage` | INT64 | Measure | The direct numerical day calculation between the current and previous stage stamps. |
| `is_sequence_violation_flag`| INT64 | Flag | Boolean-style monitoring flag (1=Error, 0=Valid) indicating out-of-order jumps. |
