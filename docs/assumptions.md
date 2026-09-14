# Assumptions and decisions

## 1. Member identity

The detailed source specification marks `Member Name` as a key column. However, the problem explicitly requires latest-record-wins behavior when a member moves countries, and the JSON feed identifies a member using `member_id`.

Therefore:

- `MEMBER_ID` is the business identity used for current-state deduplication and joins.
- `MEMBER_NAME` remains mandatory according to the source contract.
- A production implementation should confirm the authoritative source key with the upstream owner.

This is deliberately called out rather than silently changing the source specification.

## 2. Post Code discrepancy

The detailed specification defines Post Code as position 9, but the supplied flat-file detail rows contain Country, DOB, and Is_Active with no visible Post Code value. The raw layer therefore preserves the original record and the staging parser treats Post Code as nullable unless the full 11-field layout is supplied.

## 3. Recency

The assessment does not provide a source update timestamp or CDC sequence. `INGESTED_AT`, followed by batch ID and source row number as deterministic tie-breakers, is used as the available recency signal.

For production, a source update timestamp or CDC sequence should be preferred because ingestion time is not necessarily business update time.

## 4. Stale member

`STALE_MEMBER = TRUE` when days since `LAST_FLIGHT_DATE` is strictly greater than 90. A null last-flight date is treated as not stale rather than guessing a flight date.

## 5. Age

Age is birthday-aware, not simply `current_year - birth_year`. A null DOB produces a null age.

## 6. Bad dates

`TRY_TO_DATE` is used in Snowflake so malformed dates become NULL and can be surfaced by data-quality checks instead of crashing an entire batch. The source record remains available in raw.

The supplied Australian sample contains `2021-13-13`, which is intentionally invalid.

## 7. Country aliases

The sample uses `IND`, `USA`, `AU`, and `PHIL`, among others. The solution normalizes common aliases for India, USA, and Australia. Other countries route to `TABLE_OTHER` until a reference-data mapping is established.

## 8. Country-table strategy

The assessment asks for country-specific target tables. This solution uses physical target tables for demonstration. At larger scale, a reference-driven country dimension plus dynamic tables/views or a standardized partitioning strategy may be preferable to creating hundreds of manually maintained tables.

## 9. JSON/member join

Transactions are retained even when the profile does not yet exist by using a LEFT JOIN for analytics. Referential-integrity exceptions can be monitored separately.

## 10. Historical versus current state

`DIM_MEMBER_CURRENT` represents the latest known state. Raw and staging layers retain batch history. If downstream consumers need full member history, a separate SCD Type 2 dimension should be introduced rather than overloading the current-state table.

## 11. Flat-file delimiter position

The supplied detail records begin with `|D|`. After splitting on `|`, index 1 is the record type and member attributes begin at index 2. The staging SQL explicitly accounts for this leading delimiter so source positions are not shifted.
