# LOOKER STUDIO DASHBOARD EXECUTIVE SUMMARY & WALKTHROUGH
---
##### **Data Analyst:** Daniel Rodriguez III

##### **Date:** June 28, 2026
---

## 1. Dashboard Blueprint: The Analytical Story Continued
The **Project Helios: Tesla People Analytics & Funnel Reliability Suite** translates our backend database engineering into an intuitive corporate analytics product. Built as a multi-page, interactive command center, the dashboard features a responsive control header anchored by dual global filters: `department` and `structural_priority`. These filters allow leadership to instantly drill down from global corporate metrics to localized engineering teams.

The design structure follows a strict layout pattern, presenting high-level scorecards at the top of the canvas, macro distribution charts in the center, and granular data grids or heatmaps at the base. This layout guides business stakeholders naturally from high-level summaries down to granular, actionable root-cause insights.

---

## 2. Meticulous Walkthrough of Dashboard KPI & Component Metrics

### PAGE 1: Corporate Recruitment Velocity & Yield Overview
* **Data Story Focus:** Establishing baseline organizational volume, overall conversion health, and volume distributions across engineering branches.

#### KPI 1: Total Candidate Funnel Influx
* **Configuration:** `COUNT_DISTINCT(candidate_id)` | **Current Value:** `1,200`
* **Analytical Interpretation:** Establishes the true baseline volume of unique applicants processed by the platform. This metric correctly counts unique candidate profiles rather than cumulative transactional rows, providing an uninflated top-of-funnel benchmark.

#### KPI 2: Gross Operational Hires
* **Configuration:** `COUNT_DISTINCT(CASE WHEN stage_reached = 'Hired' THEN candidate_id ELSE NULL END)` | **Current Value:** `54`
* **Analytical Interpretation:** Serves as the ultimate volume measure of recruitment success, tracking total pipeline throughput that converted into verified headcount additions.

#### KPI 3: Top-to-Bottom Pipeline Yield
* **Configuration:** `Gross Operational Hires / Total Candidate Funnel Influx` | **Current Value:** `4.50%`
* **Analytical Interpretation:** Quantifies aggregate funnel conversion efficiency. This metric reveals that for every 100 applicants entering the pipeline, approximately 4.5 are successfully hired, establishing a key metric for headcount capacity forecasting.

#### Chart 1: Net Engineering Headcount Acquisition by Department
* **Configuration:** Horizontal Bar Chart | Dimension: `department` | Metric: `Gross Operational Hires` | Sort: `Gross Operational Hires (DESC)`
* **Analytical Interpretation:** Highlights team-specific hiring output. The horizontal layout instantly showcases that `Robotics` (12 hires) and `Tesla Energy` (11 hires) are leading organizational growth, while `Artificial Intelligence` (1 hire) represents the lowest absolute volume.

---

### PAGE 2: Interview Loop Velocity & Bottleneck Analysis
* **Data Story Focus:** Uncovering process constraints and evaluating operational time-in-stage aging.

#### Chart 1: Historical Stage Progression Attrition
* **Configuration:** Sequential Step Column Chart | Dimension: `stage_reached` | Metric: `COUNT_DISTINCT(candidate_id)` | Sort: `Stage Sort Metric (ASC)`
* **Analytical Interpretation:** Visually maps top-to-bottom candidate drop-off (`Applied: 1,200` $\rightarrow$ `Phone Screen: 636` $\rightarrow$ `Technical Interview: 332` $\rightarrow$ `Offer Issued: 166` $\rightarrow$ `Hired: 54`). Because it utilizes a custom numeric ranking sort, the steps flow in strict chronological order, ensuring the data narrative reads correctly from left to right.

#### Chart 2: Average Time-in-Stage Cycle Aging Matrix (Days)
* **Configuration:** Pivot Table Heatmap | Rows: `department` | Columns: `stage_reached` | Metric: `days_spent_in_prior_stage (AVG)` | Row Sort: `days_spent_in_prior_stage (DESC)` | Column Sort: `Stage Sort Metric (ASC)`
* **Analytical Interpretation:** The primary operational engine of Page 2. By displaying average days spent in each phase, it provides the visual proof for our ANOVA conclusions: stage durations remain tightly clustered between 7.7 and 9.3 days across almost all departments and phases. The matrix highlights that `Robotics` faces the most significant internal delay, taking an average of **9.32 days** to clear the `Technical Interview` loop. The initial `Applied` column is cleanly masked with null indicators (`-`), ensuring application baselines do not distort our operational averages.

---

### PAGE 3: Data Ingestion Governance & System Quality Assurance
* **Data Story Focus:** System health monitoring, data ingestion integrity, and automated pipeline governance checks.

#### Chart 1: Ingestion Integrity & Missing Attribute Audit by Sourcing Channel
* **Configuration:** Data Grid Table | Dimension: `source_channel` | Metrics: `Missing Source Flags (SUM)`, `Total Events (COUNT)` | Sort: `Missing Source Flags (DESC)`
* **Analytical Interpretation:** Acts as our data engineering control monitor. It highlights that while primary platforms like LinkedIn and the Careers Site are logging clean data, a subset of **87 events** lacked valid sourcing dimensions and were successfully routed to our fallback tag (`SYSTEM_NULL_TRIGGER`). This provides administrators with a direct list of system links that require tracking repairs.

#### Chart 2: Global Pipeline Process Compliance Index
* **Configuration:** Dial Gauge Chart | Metric: Calculated Process Compliance Rate % | Axis Bounds: `0` to `100`
* **Analytical Interpretation:** Displays a perfect **100.0%** compliance rate across our active production datasets. This confirms that all records loaded into the analytics mart match proper linear stage sequences, verifying that the data platform is completely free of chronological errors or out-of-order logging loops.

---

## 3. Resolving Project Core Questions

### Q1: Why should Page 1 Influx not match raw log row counts?
* **Resolution:** Raw data logs record every individual transaction entry step, creating multiple rows for a single applicant over time. The "Total Candidate Funnel Influx" KPI utilizes a strict `COUNT_DISTINCT` expression to count individual candidate IDs rather than tracking rows. This ensures that leadership views actual headcount figures rather than cumulative system activity logs.

### Q2: Why are null values present in the underlying data table?
* **Resolution:** Null entries in `immediate_prior_stage` and `days_spent_in_prior_stage` are logical system indicators for the initial `Applied` state. Because an applicant has no tracking history before their initial application, there is no previous milestone to reference or evaluate. Keeping these fields as true nulls is an intentional design choice; it prevents artificial zero-day values from distorting corporate cycle-time averages.

### Q3: How do we fix Looker Studio's alphabetical sorting issues?
* **Resolution:** Looker Studio defaults to alphabetical sorting for custom text fields, which can display stages out of sequence (e.g., placing `Hired` before `Phone Screen`). Project Helios resolves this by implementing an explicit numeric casting case statement (`Stage Sort Metric`) wrapped in a numeric override. This forces the chart components to sort based on numerical ranking (`1` through `5`), ensuring columns and bars line up in proper chronological order.
