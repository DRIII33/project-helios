CREATE OR REPLACE TABLE `driiiportfolio.recruiting_mart.dim_requisition`
CLUSTER BY department, priority AS
SELECT
  CAST(req_id AS STRING) AS requisition_id,
  COALESCE(hiring_manager, 'UNASSIGNED') AS hiring_manager,
  COALESCE(department, 'UNKNOWN ENGINEERING') AS department,
  location AS assignment_location,
  priority AS structural_priority,
  CAST(planned_hires AS INT64) AS planned_headcount,
  PARSE_DATE('%Y-%m-%d', requisition_open_date) AS open_date
FROM
  `driiiportfolio.recruiting_raw.raw_requisitions`;
