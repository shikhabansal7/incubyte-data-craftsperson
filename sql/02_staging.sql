-- Canonical member staging.
-- The source flat-file sample has 10 values after |D|, although the detailed
-- specification also defines Post Code. POST_CODE is therefore nullable.

CREATE OR REPLACE TABLE STG_MEMBER (
    BATCH_ID             VARCHAR(100) NOT NULL,
    SOURCE_FILE_NAME     VARCHAR(500) NOT NULL,
    SOURCE_ROW_NUMBER    NUMBER,
    MEMBER_NAME          VARCHAR(255),
    MEMBER_ID            VARCHAR(18),
    ENROLLMENT_DATE      DATE,
    LAST_FLIGHT_DATE     DATE,
    TIER_CODE            VARCHAR(5),
    AGENT_NAME            VARCHAR(255),
    STATE_CODE            VARCHAR(5),
    COUNTRY_CODE         VARCHAR(5),
    POST_CODE            NUMBER(5,0),
    DATE_OF_BIRTH        DATE,
    ACTIVE_MEMBER        VARCHAR(1),
    AGE                  NUMBER(3,0),
    STALE_MEMBER         BOOLEAN,
    INGESTED_AT           TIMESTAMP_NTZ NOT NULL,
    RECORD_HASH           VARCHAR(64)
);

-- Example transformation from RAW_MEMBER_FEED.
-- TRY_TO_DATE prevents one malformed date from aborting the entire batch.
INSERT INTO STG_MEMBER (
    BATCH_ID, SOURCE_FILE_NAME, SOURCE_ROW_NUMBER,
    MEMBER_NAME, MEMBER_ID, ENROLLMENT_DATE, LAST_FLIGHT_DATE,
    TIER_CODE, AGENT_NAME, STATE_CODE, COUNTRY_CODE, POST_CODE,
    DATE_OF_BIRTH, ACTIVE_MEMBER, AGE, STALE_MEMBER, INGESTED_AT, RECORD_HASH
)
WITH parsed AS (
    SELECT
        BATCH_ID,
        SOURCE_FILE_NAME,
        ROW_NUMBER() OVER (
            PARTITION BY BATCH_ID, SOURCE_FILE_NAME
            ORDER BY INGESTED_AT, RAW_RECORD
        ) AS SOURCE_ROW_NUMBER,
        SPLIT(RAW_RECORD, '|') AS F
        ,INGESTED_AT
    FROM RAW_MEMBER_FEED
    WHERE RECORD_TYPE = 'D'
)
SELECT
    BATCH_ID,
    SOURCE_FILE_NAME,
    SOURCE_ROW_NUMBER,
    NULLIF(TRIM(F[2]::VARCHAR), ''),
    NULLIF(TRIM(F[3]::VARCHAR), ''),
    TRY_TO_DATE(NULLIF(TRIM(F[4]::VARCHAR), ''), 'YYYYMMDD'),
    TRY_TO_DATE(NULLIF(TRIM(F[5]::VARCHAR), ''), 'YYYYMMDD'),
    NULLIF(TRIM(F[6]::VARCHAR), ''),
    NULLIF(TRIM(F[7]::VARCHAR), ''),
    NULLIF(TRIM(F[8]::VARCHAR), ''),
    NULLIF(TRIM(F[9]::VARCHAR), ''),
    NULL,
    TRY_TO_DATE(NULLIF(TRIM(F[10]::VARCHAR), ''), 'MMDDYYYY'),
    NULLIF(TRIM(F[11]::VARCHAR), ''),
    CASE
        WHEN TRY_TO_DATE(NULLIF(TRIM(F[10]::VARCHAR), ''), 'MMDDYYYY') IS NULL THEN NULL
        ELSE DATEDIFF(
            year,
            TRY_TO_DATE(NULLIF(TRIM(F[10]::VARCHAR), ''), 'MMDDYYYY'),
            CURRENT_DATE()
        )
        - IFF(
            DATE_FROM_PARTS(
                YEAR(CURRENT_DATE()),
                MONTH(TRY_TO_DATE(NULLIF(TRIM(F[10]::VARCHAR), ''), 'MMDDYYYY')),
                DAY(TRY_TO_DATE(NULLIF(TRIM(F[10]::VARCHAR), ''), 'MMDDYYYY'))
            ) > CURRENT_DATE(),
            1, 0
        )
    END,
    CASE
        WHEN TRY_TO_DATE(NULLIF(TRIM(F[5]::VARCHAR), ''), 'YYYYMMDD') IS NULL THEN FALSE
        ELSE DATEDIFF(
            day,
            TRY_TO_DATE(NULLIF(TRIM(F[5]::VARCHAR), ''), 'YYYYMMDD'),
            CURRENT_DATE()
        ) > 90
    END,
    INGESTED_AT,
    SHA2(RAW_RECORD, 256)
FROM parsed;
