SELECT 'requisitions' AS tab, COUNT(*) AS total FROM `driiiportfolio.recruiting_raw.raw_requisitions`
UNION ALL
SELECT 'events' AS tab, COUNT(*) AS total FROM `driiiportfolio.recruiting_raw.raw_pipeline_events`;
