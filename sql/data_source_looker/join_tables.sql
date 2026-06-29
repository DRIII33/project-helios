SELECT 
  f.*,
  r.department,
  r.structural_priority,
  r.assignment_location,
  r.open_date,
  rec.recruiter_name,
  rec.staffing_vertical
FROM `driiiportfolio.recruiting_mart.fact_candidate_pipeline` f
LEFT JOIN `driiiportfolio.recruiting_mart.dim_requisition` r ON f.requisition_id = r.requisition_id
LEFT JOIN `driiiportfolio.recruiting_mart.dim_recruiter` rec ON f.recruiter_id = rec.recruiter_id;
