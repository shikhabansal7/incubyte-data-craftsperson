from datetime import date, datetime
from typing import Any


COUNTRY_ALIASES = {
    "IND": "INDIA",
    "INDIA": "INDIA",
    "USA": "USA",
    "US": "USA",
    "AU": "AUS",
    "AUS": "AUS",
    "AUSTRALIA": "AUS",
}


def parse_compact_date(value: str | None, fmt: str) -> date | None:
    if not value:
        return None
    pattern = "%Y%m%d" if fmt == "YYYYMMDD" else "%m%d%Y"
    try:
        return datetime.strptime(value, pattern).date()
    except ValueError:
        return None


def calculate_age(dob: date | None, as_of: date) -> int | None:
    if dob is None:
        return None
    age = as_of.year - dob.year
    if (as_of.month, as_of.day) < (dob.month, dob.day):
        age -= 1
    return age


def is_stale(last_flight_date: date | None, as_of: date, threshold_days: int = 90) -> bool:
    if last_flight_date is None:
        return False
    return (as_of - last_flight_date).days > threshold_days


def route_country(country: str | None) -> str:
    if not country:
        return "OTHER"
    return COUNTRY_ALIASES.get(country.strip().upper(), "OTHER")


def latest_records_by_member(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    current: dict[str, dict[str, Any]] = {}
    for row in records:
        member_id = row.get("member_id")
        if member_id is None:
            continue
        previous = current.get(member_id)
        if previous is None or row.get("ingested_at", 0) > previous.get("ingested_at", 0):
            current[member_id] = row
    return current


def flatten_redemptions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    member_id = payload.get("member_id")
    feed_date = payload.get("feed_date")
    rows = []
    for redemption in payload.get("redemptions", []):
        rows.append(
            {
                "member_id": member_id,
                "feed_date": feed_date,
                "txn_id": redemption.get("txn_id"),
                "txn_date": redemption.get("txn_date"),
                "partner": redemption.get("partner"),
                "miles_redeemed": redemption.get("miles_redeemed"),
                "status": redemption.get("status"),
            }
        )
    return rows


def validate_member(row: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if not row.get("member_name") or not row.get("member_id") or not row.get("enrollment_date"):
        errors.append(
            {
                "check": "MANDATORY_MEMBER_FIELDS",
                "severity": "ERROR",
                "message": "Member_Name, Member_ID, and Enrollment_Date are mandatory",
            }
        )

    tier = row.get("tier_code")
    if tier and tier.upper() not in {"PLT", "GLD", "SLV"}:
        errors.append(
            {
                "check": "TIER_CODE_DOMAIN",
                "severity": "ERROR",
                "message": "Tier_Code must be PLT, GLD, or SLV",
            }
        )

    active = row.get("active_member")
    if active and active.upper() not in {"A", "I"}:
        errors.append(
            {
                "check": "ACTIVE_MEMBER_DOMAIN",
                "severity": "ERROR",
                "message": "Active Member must be A or I",
            }
        )

    enrollment = row.get("enrollment_date")
    flight = row.get("last_flight_date")
    if enrollment and flight and enrollment > flight:
        errors.append(
            {
                "check": "DATE_CONSISTENCY",
                "severity": "ERROR",
                "message": "Enrollment date cannot be after last flight date",
            }
        )

    if row.get("date_of_birth") is None:
        errors.append(
            {
                "check": "OPTIONAL_DOB_MISSING",
                "severity": "WARNING",
                "message": "Date of birth is missing",
            }
        )

    return errors
