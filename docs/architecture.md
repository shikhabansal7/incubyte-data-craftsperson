# Architecture

## Logical flow

```text
             +-------------------+
             | Source flat feed  |
             +---------+---------+
                       |
                       v
             +-------------------+
             | RAW_MEMBER_FEED   |
             | immutable payload |
             +---------+---------+
                       |
                       v
             +-------------------+
             |   STG_MEMBER      |
             | parse + standardize
             | age + stale flag  |
             +---------+---------+
                       |
                       v
             +-------------------+
             | DIM_MEMBER_CURRENT|
             | latest by MEMBER_ID
             +---------+---------+
                       |
          +------------+-------------+
          |            |             |
          v            v             v
     TABLE_INDIA   TABLE_USA    TABLE_AUS
          |
          +------> TABLE_OTHER

 Source JSON
      |
      v
 RAW_REDEMPTION_FEED
      |
      v
 FACT_REDEMPTION <------ DIM_MEMBER_CURRENT
      |
      v
 analytics / downstream consumers
```

## Why the raw layer matters

Raw data is retained before business transformations. This makes the pipeline replayable, auditable, and easier to troubleshoot when a source contract changes.

## Why staging is canonical

The assessment contains multiple sample formats. A canonical staging model isolates source-specific parsing from downstream business logic. For example, the supplied India sample uses `M/D/YYYY`, while the US sample uses compact `MMDDYYYY`.

## Latest-record-wins

A member can change country. The current-state table selects one record per `MEMBER_ID`, ordered by ingestion recency. Country tables are populated from this current-state table rather than independently appending every historical record.

This prevents a moved member from remaining current in the previous country.

## JSON model

The partner feed has one member object containing a redemption array. `LATERAL FLATTEN` turns the nested array into one transaction row per redemption. `MEMBER_ID` is the join key to the current member dimension.

A `LEFT JOIN` is recommended for analytics so a valid transaction is not lost solely because its member profile is delayed.
