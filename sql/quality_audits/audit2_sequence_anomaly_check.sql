-- Audit Query 2: Enterprise Funnel Conversion Analytics (Aligned)
-- This query maps candidate conversion across your key hiring stages:

SELECT
  r.department,
  f.source_channel,
  COUNT(DISTINCT CASE WHEN f.stage_reached = 'Applied' THEN f.candidate_id END) AS total_applicants,
  COUNT(DISTINCT CASE WHEN f.stage_reached = 'Phone Screen' THEN f.candidate_id END) AS total_screens,
  COUNT(DISTINCT CASE WHEN f.stage_reached = 'Technical Interview' THEN f.candidate_id END) AS total_technical_interviews,
  COUNT(DISTINCT CASE WHEN f.stage_reached = 'Offer Issued' THEN f.candidate_id END) AS total_offers,
  COUNT(DISTINCT CASE WHEN f.stage_reached = 'Hired' THEN f.candidate_id END) AS total_hires,
  SAFE_DIVIDE(COUNT(DISTINCT CASE WHEN f.stage_reached = 'Hired' THEN f.candidate_id END), 
              COUNT(DISTINCT CASE WHEN f.stage_reached = 'Applied' THEN f.candidate_id END)) * 100 AS gross_conversion_rate
FROM
  `driiiportfolio.recruiting_mart.fact_candidate_pipeline` f
JOIN
  `driiiportfolio.recruiting_mart.dim_requisition` r ON f.requisition_id = r.requisition_id
GROUP BY 1, 2
ORDER BY total_applicants DESC;
