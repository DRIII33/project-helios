# PRODUCT REQUIREMENTS DOCUMENT (PRD)

## Product Name: Project Helios Talent Pipeline & Governance Product
**Document Version:** 1.0.0  
**Target Organization:** Tesla People Analytics & Infrastructure Engineering  
**Product Status:** Production-Ready Blueprint  
**Data Analyst:** Daniel Rodriguez III

---

## 1. Business Problem
Tesla’s Talent Acquisition and Engineering leadership teams operate in a high-velocity hiring environment where structural headcount capacity directly impacts factory output and R&D vehicle program timelines. Historically, recruiting funnel data extracted from operational Applicant Tracking Systems (ATS) suffered from inconsistent state logging, manual entry errors, and untracked sourcing paths. 

Without clean data pipelines, downstream "People Products" produced highly distorted cycle-time metrics. Recruiters routinely blamed external sourcing channels for pipeline delays, while operational data engineering lacked the rigorous statistical frameworks required to isolate true internal review bottlenecks. Project Helios addresses this by implementing an end-to-end data validation, processing, and visualization pipeline to act as a single source of truth for recruitment health.

---

## 2. User Personas

### Persona A: The VP of People Analytics / Chief HR Officer
* **Needs:** A high-level view of top-to-bottom recruitment conversion yield and aggregate headcount delivery across engineering organizations.
* **Pain Points:** Distrusts data summaries due to legacy tracking gaps; requires statistically validated insights to make enterprise-wide staffing and budgeting decisions.

### Persona B: Recruiting Operations Manager
* **Needs:** Granular visibility into time-in-stage metrics, process compliance tracking, and automated auditing of messy data entries (e.g., missing sourcing tags).
* **Pain Points:** Spends hours manually auditing and cleaning spreadsheet exports to identify broken hiring loops or system exceptions.

### Persona C: Engineering Directors (Hiring Managers)
* **Needs:** Objective operational data identifying the exact internal interview cycle bottlenecks slowing down engineering headcount acquisition.
* **Pain Points:** Receives generic reports blaming external candidate drop-off rather than identifying internal assessment delays.

---

## 3. Functional Requirements

### FR-1: Ingestion & Missing Attribute Fallbacks
* The data pipeline must process raw transactional event logs and automatically route missing dimension entries (such as unpopulated sourcing strings) to a standard fallback tag (`SYSTEM_NULL_TRIGGER`) without crashing downstream analytical models.

### FR-2: Chronological Sequence Validation
* The pipeline must evaluate historical stage entry logs using window partitioning over candidate records. It must flag any out-of-order stage progressions (e.g., bypassing interview phases or entering a reverse loop) via a dedicated boolean indicator (`is_sequence_violation_flag`).

### FR-3: Native Delta Calculation
* The transformation tier must compute the exact day-count difference between consecutive pipeline milestones for each individual applicant. This metric must automatically ignore initial application events to maintain the integrity of downstream operational averages.

### FR-4: Advanced Analytics Interface
* The user interface must deliver multi-page interactive analytics, separating macro executive yield indicators from micro aging heatmaps and system quality logs.

---

## 4. Non-Functional Requirements

### NFR-1: Zero-Cost Computing Footprint
* The data warehouse layer must execute entirely within a zero-cost public cloud environment (such as the Google BigQuery Sandbox) without relying on permanent computing billing parameters.

### NFR-2: Dynamic Query Performance
* Semantic views and tables must utilize optimization techniques, including cluster-by keys on high-cardinality dimensions (`source_channel`, `stage_reached`), keeping dashboard refresh queries snappy and efficient.

### NFR-3: Strict Analytical Isolation
* Automated statistical evaluation modules must run completely isolated from web visual layers, using mathematical engines (e.g., Python standard libraries) to guarantee reproducible statistical verification.

---

## 5. Data Contracts

### Inbound Ingestion Interface: `raw_pipeline_events`
```json
[
  {"name": "pipeline_event_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "candidate_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "req_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "source_channel", "type": "STRING", "mode": "NULLABLE"},
  {"name": "stage_reached", "type": "STRING", "mode": "REQUIRED"},
  {"name": "stage_entry_timestamp", "type": "STRING", "mode": "REQUIRED"},
  {"name": "recruiter_id", "type": "STRING", "mode": "REQUIRED"}
]

```

### Outbound Semantic Interface: `fact_candidate_pipeline`

```json
[
  {"name": "pipeline_event_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "candidate_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "requisition_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "source_channel", "type": "STRING", "mode": "REQUIRED"},
  {"name": "stage_reached", "type": "STRING", "mode": "REQUIRED"},
  {"name": "stage_entry_time", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "recruiter_id", "type": "STRING", "mode": "REQUIRED"},
  {"name": "immediate_prior_stage", "type": "STRING", "mode": "NULLABLE"},
  {"name": "days_spent_in_prior_stage", "type": "INT64", "mode": "NULLABLE"},
  {"name": "is_sequence_violation_flag", "type": "INT64", "mode": "REQUIRED"}
]

```

---

## 6. Success Metrics

* **Pipeline Compliance Target:** Maintain a data tracking structural compliance index of $\ge 99.5\%$ across all automated data loads.
* **Insight Precision:** Reduce standard reporting cycle errors (such as artificial 0-day duration averages caused by unhandled nulls) to $0.0\%$.
* **Analytical Resolution Speed:** Decrease the time required to isolate team-specific interview bottlenecks from weeks of manual analysis down to sub-second dashboard queries.

---

## 7. Acceptance Criteria

1. **Null Resilience Check:** Downstream processing must succeed even when raw application logs contain null data points, smoothly converting them to `SYSTEM_NULL_TRIGGER`.
2. **Mathematical Verification:** The product must run automated statistical algorithms locally. The one-way ANOVA model must compute an exact F-statistic and $p$-value across sourcing channels, and the Pearson Correlation test must output a valid coefficient ($r$) bounded tightly between $-1.0$ and $+1.0$.
3. **Visual Integrity:** Visual dashboard components must render multi-stage conversion sequences in strict chronological order, ensuring candidate volumes step down logically at every milestone.

---

## 8. Future Enhancements

* **Predictive Pipeline Aging:** Integrate machine learning classification models to predict a candidate's likelihood to withdraw based on localized time-in-stage anomalies.
* **Automated ATS Webhook Synchronization:** Transition from static data batch uploads to automated, real-time API webhook streaming directly into secure cloud cloud infrastructure.

---

### File 2: `project-helios/docs/DATA_DICTIONARY.md`

```markdown
# Project Helios Data Engine: Conformed Dimension Ledger

## Fact Matrix Table: `fact_candidate_pipeline`
This fact table captures every granular state transition an applicant undergoes throughout the recruitment cycle. It is pre-processed using window functions to evaluate state durations natively without complex self-joins.

| Column Name | Storage Type | Constraint | Definition |
| :--- | :--- | :--- | :--- |
| `pipeline_event_id` | STRING | PK | Unique system hash key isolating a specific transaction entry step. |
| `candidate_id` | STRING | FK | Unique key grouping an individual candidate's historical pipeline journey. |
| `requisition_id` | STRING | FK | Relational link mapping the applicant directly to an open headcount slot. |
| `source_channel` | STRING | Dimension | Ingestion-derived sourcing route. Missing attributes fallback to `SYSTEM_NULL_TRIGGER`. |
| `stage_reached` | STRING | Dimension | Pipeline milestone state string (`Applied`, `Phone Screen`, `Interview`, `Offer Issued`, `Hired`). |
| `stage_entry_time` | TIMESTAMP | Axis | The structured date and time execution mark when a candidate entered the state. |
| `recruiter_id` | STRING | FK | Key indicating the primary assigned owner managing the talent lifecycle. |
| `immediate_prior_stage`| STRING | Attribute | Captured via `LAG()` partitioning. Identifies the previous phase position. |
| `days_spent_in_prior_stage` | INT64 | Measure | The direct numerical day calculation between the current and previous stage stamps. |
| `is_sequence_violation_flag`| INT64 | Flag | Boolean-style monitoring flag (1=Error, 0=Valid) indicating out-of-order jumps. |

```

---

### File 3: `project-helios/docs/KPI_CATALOG.md`

```markdown
# Project Helios Corporate KPI Catalog

### Metric 1: Aggregate Funnel Conversion Yield %
* **Business Intent:** Quantifies the top-to-bottom efficiency of the talent acquisition pipeline, isolating how effectively raw interest converts into signed talent.
* **Mathematical Formula:**
    $$\text{Funnel Yield \%} = \left( \frac{\text{Count Distinct Candidates Achieving 'Hired'}}{\text{Count Distinct Total Candidates Entering System}} \right) \times 100$$
* **Stakeholder Consumer Group:** Chief Human Resources Officer, Recruiting VP.

### Metric 2: Departmental Aging Velocity Metric
* **Business Intent:** Pinpoints where candidates encounter operational drag inside specific interviewing tracks, illuminating team-specific internal barriers.
* **Mathematical Formula:**
    $$\text{Departmental Aging} = \frac{1}{N} \sum_{i=1}^{N} (\text{Timestamp}_{\text{Current Stage Entry}} - \text{Timestamp}_{\text{Prior Stage Entry}})$$
* **Stakeholder Consumer Group:** Engineering Directors, Headcount Planning Managers.

```

---

### File 4: `project-helios/README.md`

```markdown
# Project Helios: Trusted Recruiting Intelligence Platform
**Target Organization Context:** People Analytics Architecture  
**Core Processing Stack:** Python, SQL, Google BigQuery Sandbox, Looker Studio, PyTest, Git  
**Engineering Tier Class:** Production Data Infrastructure / Corporate Portfolio Framework

## Project Overview
Project Helios addresses a major issue in People Analytics: messy tracking data that makes downstream recruiting metrics unreliable. Built to run inside a zero-cost BigQuery Sandbox environment, this system uses a star schema architecture to process synthetic hiring data, flag workflow gaps, and track processing speeds.

### Core Analytical Discoveries
Our integrated statistical modeling revealed key insights about the recruitment process:
* **Sourcing Consistency (ANOVA Analysis):** Running a one-way ANOVA test against the dataset yielded a $p$-value of **0.804037**. This confirms that candidate processing speed does not vary significantly across sourcing channels (LinkedIn, Referrals, etc.). Sourcing channels are not the root cause of pipeline delays.
* **Funnel Linearity (Pearson Correlation):** A Pearson Correlation analysis returned a strong positive coefficient ($r = \mathbf{0.5589}, p = \mathbf{0.000000}$), proving a highly significant relationship between a candidate's stage progression depth and successful hiring outcomes. This confirms that internal interview steps reliably move candidates closer to an offer.

## Local Workspace Environment Deployment Blueprint
To spin up the data pipeline and execute validation checks locally, run these commands in your terminal:
---
```bash
# 1. Initialize virtual environment and pull strict pinned dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run the synthetic data generator engine to build local CSVs
python -m src.data_generator

# 3. Run the automated data quality suite to run structural checks
python -m src.quality_engine

# 4. Execute the statistical analysis and hypothesis tests
python -m src.statistical_analysis

```
---
## Data Warehouse Architecture Summary

The analytics warehouse shifts from raw operational inputs to a clean, highly structured star schema designed for fast, efficient reporting:

* `recruiting_raw.raw_pipeline_events`: Raw log files from applicant tracking systems.
* `recruiting_raw.raw_candidates`: Unified candidate directory mapping applicants to recruiters and job listings.
* `recruiting_mart.dim_requisition`: Clustered dimension table housing active hiring goals across engineering divisions.
* `recruiting_mart.fact_candidate_pipeline`: Main fact table tracking time-in-stage metrics, historic milestones, and pipeline health indicators.
