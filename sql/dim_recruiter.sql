CREATE OR REPLACE TABLE `driiiportfolio.recruiting_mart.dim_recruiter` AS
SELECT
  CAST(recruiter_id AS STRING) AS recruiter_id,
  recruiter_name,
  team AS staffing_vertical
FROM
  `driiiportfolio.recruiting_raw.raw_recruiters`;
