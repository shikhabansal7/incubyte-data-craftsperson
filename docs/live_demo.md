# Live Demo Runbook

## 1. Start with the problem

Explain that SkyPoints receives two daily feeds and needs country-specific member targets while supporting very large volumes.

## 2. Show the raw layer

Point to:

- `RAW_MEMBER_FEED`
- `RAW_REDEMPTION_FEED`
- batch ID
- source filename
- ingestion timestamp

Explain that raw preservation supports replay and auditability.

## 3. Show staging

Run a sample query:

```sql
SELECT
    MEMBER_ID,
    MEMBER_NAME,
    ENROLLMENT_DATE,
    LAST_FLIGHT_DATE,
    AGE,
    STALE_MEMBER
FROM STG_MEMBER
ORDER BY MEMBER_ID;
```

Explain that parsing uses safe date conversion and derives age/staleness.

## 4. Demonstrate bad data

Show the Australian invalid enrollment date and NULL DOB. Explain that malformed dates become NULL and are reported by DQ rather than aborting the batch.

## 5. Demonstrate movement

Insert two records for one member with different countries and ingestion timestamps. Rebuild `DIM_MEMBER_CURRENT`.

Show that only the latest country is represented in the country targets.

## 6. Demonstrate JSON flattening

Run:

```sql
SELECT *
FROM FACT_REDEMPTION
ORDER BY TXN_DATE, TXN_ID;
```

Then show the join:

```sql
SELECT
    f.TXN_ID,
    f.MEMBER_ID,
    m.MEMBER_NAME,
    m.COUNTRY_CODE,
    f.MILES_REDEEMED
FROM FACT_REDEMPTION f
LEFT JOIN DIM_MEMBER_CURRENT m
    ON f.MEMBER_ID = m.MEMBER_ID;
```

## 7. Close with scale

Emphasize:

- set-based SQL
- incremental batches
- raw/staging separation
- deterministic deduplication
- persisted DQ results
- idempotent current-state rebuild
- operational auditability

Avoid claiming a benchmark that has not been measured.
