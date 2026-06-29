CREATE OR REPLACE TABLE `driiiportfolio.recruiting_mart.fact_candidate_pipeline`
CLUSTER BY source_channel, stage_reached AS
WITH ordered_pipeline AS (
  SELECT
    pipeline_event_id,
    candidate_id,
    req_id AS requisition_id,
    COALESCE(source_channel, 'SYSTEM_NULL_TRIGGER') AS source_channel,
    stage_reached,
    PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', stage_entry_timestamp) AS stage_entry_time,
    recruiter_id,
    LAG(stage_reached) OVER(PARTITION BY candidate_id ORDER BY PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', stage_entry_timestamp)) AS immediate_prior_stage,
    LAG(PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', stage_entry_timestamp)) OVER(PARTITION BY candidate_id ORDER BY PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', stage_entry_timestamp)) AS prior_stage_exit_time
  FROM
    `driiiportfolio.recruiting_raw.raw_pipeline_events`
)
SELECT
  p.pipeline_event_id,
  p.candidate_id,
  p.requisition_id,
  p.source_channel,
  p.stage_reached,
  p.stage_entry_time,
  p.recruiter_id,
  p.immediate_prior_stage,
  -- FIXED: Removed redundant PARSE_TIMESTAMP to allow direct evaluation of the intervals
  TIMESTAMP_DIFF(p.stage_entry_time, p.prior_stage_exit_time, DAY) AS days_spent_in_prior_stage,
  CASE 
    WHEN p.immediate_prior_stage IS NULL AND p.stage_reached != 'Applied' THEN 1
    WHEN p.immediate_prior_stage = 'Applied' AND p.stage_reached NOT IN ('Phone Screen', 'Technical Interview', 'Offer Issued', 'Hired') THEN 1
    ELSE 0
  END AS is_sequence_violation_flag
FROM
  ordered_pipeline p;
