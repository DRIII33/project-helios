# Project Helios Corporate KPI Catalog

## Metric 1: Aggregate Funnel Conversion Yield (%)

### Business Intent
Quantifies the top-to-bottom efficiency of the talent acquisition pipeline, isolating how effectively raw interest converts into signed talent.

### Formula

```text
Funnel Yield (%) =
(
  Count Distinct Candidates Achieving "Hired"
  ÷
  Count Distinct Total Candidates Entering System
) × 100
```

### Stakeholder Consumer Group
- Chief Human Resources Officer (CHRO)
- Recruiting Vice President (VP)

---

## Metric 2: Departmental Aging Velocity Metric

### Business Intent
Pinpoints where candidates encounter operational drag inside specific interviewing tracks, illuminating team-specific internal barriers.

### Formula

```text
Departmental Aging =
(1 / N) × Σ(
  Timestamp(Current Stage Entry)
  -
  Timestamp(Prior Stage Entry)
)
```

Where:

- **N** = Total candidate observations included in the calculation
- **Σ** = Summation across all observations

### Stakeholder Consumer Group
- Engineering Directors
- Headcount Planning Managers
