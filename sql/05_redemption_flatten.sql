-- Flatten partner JSON into one row per redemption transaction.

CREATE OR REPLACE TABLE FACT_REDEMPTION (
    BATCH_ID         VARCHAR(100) NOT NULL,
    SOURCE_FILE_NAME VARCHAR(500) NOT NULL,
    MEMBER_ID        VARCHAR(18),
    FEED_DATE        DATE,
    TXN_ID           VARCHAR(100),
    TXN_DATE         DATE,
    PARTNER          VARCHAR(255),
    MILES_REDEEMED   NUMBER(18,0),
    STATUS           VARCHAR(30),
    INGESTED_AT      TIMESTAMP_NTZ NOT NULL
);

INSERT INTO FACT_REDEMPTION (
    BATCH_ID, SOURCE_FILE_NAME, MEMBER_ID, FEED_DATE,
    TXN_ID, TXN_DATE, PARTNER, MILES_REDEEMED, STATUS, INGESTED_AT
)
SELECT
    r.BATCH_ID,
    r.SOURCE_FILE_NAME,
    r.RAW_PAYLOAD:member_id::VARCHAR,
    TRY_TO_DATE(r.RAW_PAYLOAD:feed_date::VARCHAR, 'YYYYMMDD'),
    red.value:txn_id::VARCHAR,
    TRY_TO_DATE(red.value:txn_date::VARCHAR, 'YYYYMMDD'),
    red.value:partner::VARCHAR,
    TRY_TO_NUMBER(red.value:miles_redeemed),
    red.value:status::VARCHAR,
    r.INGESTED_AT
FROM RAW_REDEMPTION_FEED r,
LATERAL FLATTEN(INPUT => r.RAW_PAYLOAD:redemptions) red;

-- Join to current profile when member attributes are required:
--
-- SELECT f.*, m.MEMBER_NAME, m.COUNTRY_CODE, m.TIER_CODE
-- FROM FACT_REDEMPTION f
-- LEFT JOIN DIM_MEMBER_CURRENT m
--   ON f.MEMBER_ID = m.MEMBER_ID;
--
-- LEFT JOIN is intentional: transactions should remain queryable even if
-- the corresponding member profile is missing or delayed.
