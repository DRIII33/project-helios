-- Audit Query 3: Calculating Phase Transitions and Stage Aging (Aligned)
-- This query calculates how long candidates stay in each stage before moving forward:

SELECT
  r.department,
  f.stage_reached,
  ROUND(AVG(f.days_spent_in_prior_stage), 1) AS mean_days_aging_in_state,
  MAX(f.days_spent_in_prior_stage) AS peak_boundary_days_spent
FROM
  `driiiportfolio.recruiting_mart.fact_candidate_pipeline` f
JOIN
  `driiiportfolio.recruiting_mart.dim_requisition` r ON f.requisition_id = r.requisition_id
WHERE f.days_spent_in_prior_stage IS NOT NULL
GROUP BY 1, 2
ORDER BY mean_days_aging_in_state DESC;
