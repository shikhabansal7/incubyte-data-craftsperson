# Data Quality Strategy

## Severity

- **ERROR** — violates a required contract or makes the record unsafe for downstream use.
- **WARNING** — usable but incomplete or requiring attention.

## Checks

| Check | Severity | Reason |
|---|---|---|
| Member name present | Error | Mandatory |
| Member ID present | Error | Required for identity/join |
| Enrollment date present | Error | Mandatory |
| Member ID uniqueness within batch | Error | Prevent ambiguous source state |
| Tier in PLT/GLD/SLV | Error | Domain control |
| Active flag in A/I | Error | Domain control |
| Enrollment <= last flight | Error | Temporal consistency |
| DOB not future | Error | Temporal validity |
| Missing DOB | Warning | DOB is optional in specification |
| Missing country | Warning | Cannot route to a named country |
| Redemption required fields | Error | Required transaction identity |
| Redemption miles > 0 | Error | Business sanity |
| Transaction date <= feed date | Error | Temporal consistency |
| Transaction ID uniqueness | Error | Prevent duplicate transactions |

## Sample issues deliberately caught

- Australian `Jonnathan` has enrollment date `2021-13-13`, which cannot be parsed as a valid date.
- Australian `Mike` has a NULL DOB; this is a warning because DOB is optional.
- Indian dates use slash-separated values.
- US dates are compact values without separators.

## Quarantine principle

Do not throw away a bad source record merely because a field fails validation. Preserve the original in raw, expose the issue in the DQ table, and only exclude records from downstream current-state targets when required for safety.
