# Incubyte Data Craftsperson — SkyPoints

A production-oriented reference implementation for the Incubyte Data Engineer technical assessment.

## Solution at a glance

The pipeline uses a layered Snowflake design:

1. **Raw/Landing** — preserve source records/payloads plus ingestion metadata.
2. **Staging** — normalize the heterogeneous member feeds into one canonical schema and derive `AGE` and `STALE_MEMBER`.
3. **Current Member** — deduplicate with a deterministic latest-record-wins rule.
4. **Country Targets** — materialize the current member population into country-specific tables.
5. **Redemptions** — flatten the partner JSON array into one row per transaction.
6. **Data Quality** — record validation failures/warnings instead of silently discarding bad data.

The repository deliberately keeps the core transformation logic in SQL and uses Python/PyTest for deterministic unit tests that do not require a Snowflake account.

## Repository structure

```text
incubyte-data-craftsperson/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw_member_feed.txt
│   ├── AUS.csv
│   ├── IND.csv
│   ├── USA.csv
│   └── redemption.json
├── sql/
│   ├── 01_raw_tables.sql
│   ├── 02_staging.sql
│   ├── 03_current_member.sql
│   ├── 04_country_targets.sql
│   ├── 05_redemption_flatten.sql
│   ├── 06_data_quality.sql
│   └── 07_pipeline_run.sql
├── tests/
│   ├── conftest.py
│   ├── test_dates_and_age.py
│   ├── test_country_routing.py
│   ├── test_json_parser.py
│   └── test_validations.py
└── docs/
    ├── architecture.md
    ├── assumptions.md
    ├── data_quality.md
    └── live_demo.md
```

## Running the tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

No cloud credentials are required for the unit-test suite.

## Snowflake execution order

Run the SQL scripts in this order after creating a database/schema:

```text
01_raw_tables.sql
02_staging.sql
03_current_member.sql
04_country_targets.sql
05_redemption_flatten.sql
06_data_quality.sql
07_pipeline_run.sql
```

`07_pipeline_run.sql` is an orchestration/reference script showing how the layers fit together. In production, the same SQL would normally be invoked by a scheduler/orchestrator with batch parameters.

## Important source-data observations

The assessment specification says `Member Name` is the key column, while the business requirement to resolve country movement requires a stable member identity. This implementation therefore uses `MEMBER_ID` as the **business identity for deduplication and joins**, while retaining the source specification and validating the source key constraints separately. The rationale is documented in `docs/assumptions.md`.

The detailed specification includes `Post Code`, but the supplied sample flat-file rows contain no Post Code field. The parser supports both the supplied 10-value detail shape and the fully specified 11-field shape without inventing a Post Code.

The supplied country samples intentionally contain quality issues: an invalid Australian enrollment date (`2021-13-13`) and a NULL DOB for Mike; the Indian sample uses slash-separated dates; and the US sample uses compact dates. These are treated as test/validation cases rather than silently corrected.

## Scalability

The design is intended for very large daily feeds:

- Raw storage is append-oriented and batch-aware.
- Transformations are set-based SQL rather than row-by-row Python loops.
- `ROW_NUMBER` performs deterministic latest-record selection.
- Country routing is based on the current member state, so a moved member is no longer current in the old country.
- JSON is flattened once into a transaction fact table.
- Batch IDs and source file names make reruns traceable.
- Validation results are persisted for operational monitoring.
- In a production deployment, incremental ingestion, Snowflake warehouse sizing, micro-partition pruning, and task/orchestrator controls should be tuned using observed workload characteristics.

## AI-assisted development

AI tools were intentionally used to accelerate the work, brainstorm implementation options, identify edge cases, propose test cases, and improve documentation. The resulting design was reviewed against the assessment specification and the supplied sample data. AI output was treated as a drafting aid rather than an authority; SQL assumptions and validation behavior are explicitly documented and covered by tests where practical.

## Live-demo focus

For an interview walkthrough, demonstrate:

1. Raw record preservation and batch metadata.
2. Canonical staging conversion and derived attributes.
3. Invalid-date handling without query failure.
4. Latest-record-wins country movement.
5. JSON `LATERAL FLATTEN`.
6. Data-quality results.
7. How the design changes when volume moves from millions to billions of records.
