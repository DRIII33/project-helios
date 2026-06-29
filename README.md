# Project Helios: Trusted Recruiting Intelligence Platform

**Target Organization Context:** People Analytics Architecture
**Core Processing Stack:** Python, SQL, Google BigQuery Sandbox, Looker Studio, PyTest, Git
**Engineering Tier Class:** Production Data Infrastructure / Corporate Portfolio Framework
**Data Analyst:** Daniel Rodriguez III
**Date:** June 28, 2026

---

## Project Overview

Project Helios addresses a major challenge in People Analytics: inconsistent and fragmented recruiting data that reduces the reliability of downstream hiring metrics. Built entirely within a zero-cost Google BigQuery Sandbox environment, the platform leverages a star schema architecture to process synthetic recruiting data, identify workflow bottlenecks, monitor candidate progression, and measure operational efficiency throughout the hiring lifecycle.

---

## Core Analytical Discoveries

Integrated statistical modeling revealed several important insights about recruitment pipeline behavior.

### Sourcing Consistency (ANOVA Analysis)

A one-way Analysis of Variance (ANOVA) test was performed to determine whether candidate processing speed differed significantly across sourcing channels.

**Result:**

```text
p-value = 0.804037
```

**Interpretation:**

Because the p-value is substantially greater than the conventional significance threshold of 0.05, there is no statistically significant difference in candidate processing speed among sourcing channels such as:

* LinkedIn
* Employee Referrals
* Job Boards
* Direct Applications

This finding suggests that sourcing channels are not a primary contributor to recruitment pipeline delays.

---

### Funnel Linearity (Pearson Correlation Analysis)

A Pearson Correlation analysis was conducted to evaluate the relationship between candidate progression depth and successful hiring outcomes.

**Result:**

```text
Correlation Coefficient (r) = 0.5589
p-value = 0.000000
```

**Interpretation:**

The analysis demonstrates a moderate-to-strong positive correlation between progression through recruiting stages and eventual hiring success.

Key observations:

* Candidates advancing deeper into the interview process are substantially more likely to be hired.
* The relationship is highly statistically significant.
* Internal recruiting stages serve as reliable indicators of eventual hiring outcomes.

---

## Local Workspace Environment Deployment Blueprint

To initialize the platform locally and execute all validation workflows, run the following commands from a terminal session.

```bash
# 1. Create a virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Generate synthetic recruiting datasets
python -m src.data_generator

# 3. Execute automated data quality validation checks
python -m src.quality_engine

# 4. Run statistical analyses and hypothesis testing
python -m src.statistical_analysis
```

---

## Platform Capabilities

### Data Generation

* Generates synthetic recruiting and hiring datasets
* Produces realistic candidate lifecycle records
* Supports reproducible testing and experimentation

### Data Quality Framework

* Structural validation testing
* Missing-value detection
* Business rule enforcement
* Pipeline integrity verification

### Statistical Analytics

* One-Way ANOVA Testing
* Pearson Correlation Analysis
* Hiring Funnel Performance Evaluation
* Candidate Progression Analysis

### Reporting & Visualization

* Google BigQuery analytical warehouse
* Looker Studio executive dashboards
* Recruiting KPI monitoring
* Operational performance tracking

---

## Architectural Objectives

Project Helios was designed to demonstrate production-oriented data engineering and analytics practices, including:

* Star schema data modeling
* Automated data quality controls
* Statistical hypothesis testing
* Reproducible analytics workflows
* Executive KPI reporting
* Cloud-native analytical infrastructure

The platform serves as a portfolio-grade example of how modern People Analytics teams can transform raw recruiting data into trusted business intelligence.
