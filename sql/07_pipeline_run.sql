-- Reference orchestration.
-- A production implementation would parameterize BATCH_ID and execute each
-- stage through an orchestrator/task graph with retry and audit handling.

-- 1. Load raw member file into RAW_MEMBER_FEED.
-- 2. Load JSON payload into RAW_REDEMPTION_FEED.
-- 3. Execute 02_staging.sql.
-- 4. Execute 03_current_member.sql.
-- 5. Execute 04_country_targets.sql.
-- 6. Execute 05_redemption_flatten.sql.
-- 7. Execute 06_data_quality.sql.
-- 8. Update ETL_BATCH_AUDIT with counts and status.

-- Recommended production control:
-- - Reject only records that violate structural safety requirements.
-- - Keep malformed business records in staging/DQ quarantine where possible.
-- - Make each batch identifiable and replayable.
-- - Do not depend on CURRENT_DATE for historical backfills; pass an effective
--   processing date into the transformation.
