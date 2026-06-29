-- Location: sql/quality_audits/sequence_anomaly_check.sql
WITH stage_ranks AS (
  SELECT
    source_channel,
    stage_reached,
    candidate_id,
    stage_entry_time,
    -- Assign numerical ranks to check linear order
    CASE stage_reached
      WHEN 'Applied' THEN 1
      WHEN 'Phone Screen' THEN 2
      WHEN 'Technical Interview' THEN 3
      WHEN 'Offer Issued' THEN 4
      WHEN 'Hired' THEN 5
      ELSE 0
    END AS current_stage_rank,
    LAG(CASE stage_reached
          WHEN 'Applied' THEN 1
          WHEN 'Phone Screen' THEN 2
          WHEN 'Technical Interview' THEN 3
          WHEN 'Offer Issued' THEN 4
          WHEN 'Hired' THEN 5
          ELSE 0
        END) OVER(PARTITION BY candidate_id ORDER BY stage_entry_time) AS prior_stage_rank
  FROM 
    `driiiportfolio.recruiting_mart.fact_candidate_pipeline`
)
SELECT 
  source_channel,
  stage_reached,
  COUNT(CASE WHEN current_stage_rank < prior_stage_rank THEN 1 END) AS reverse_loop_count,
  COUNT(CASE WHEN current_stage_rank - prior_stage_rank > 1 THEN 1 END) AS skipped_stage_count,
  COUNT(CASE WHEN source_channel = 'SYSTEM_NULL_TRIGGER' THEN 1 END) AS missing_source_count,
  COUNT(*) AS total_stage_events
FROM 
  stage_ranks
GROUP BY 1, 2
ORDER BY total_stage_events DESC;
