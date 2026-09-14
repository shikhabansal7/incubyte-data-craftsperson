from src_logic import validate_member


def test_mandatory_fields_are_errors():
    errors = validate_member(
        {"member_name": None, "member_id": "1", "enrollment_date": None}
    )
    assert any(e["check"] == "MANDATORY_MEMBER_FIELDS" for e in errors)


def test_null_dob_is_warning_not_error():
    errors = validate_member(
        {
            "member_name": "Mike",
            "member_id": "1",
            "enrollment_date": "2022-08-01",
            "date_of_birth": None,
        }
    )
    dob_errors = [e for e in errors if e["check"] == "OPTIONAL_DOB_MISSING"]
    assert len(dob_errors) == 1
    assert dob_errors[0]["severity"] == "WARNING"


def test_invalid_tier_is_error():
    errors = validate_member(
        {
            "member_name": "Test",
            "member_id": "1",
            "enrollment_date": "2022-01-01",
            "tier_code": "BAD",
        }
    )
    assert any(e["check"] == "TIER_CODE_DOMAIN" for e in errors)


def test_enrollment_after_flight_is_error():
    errors = validate_member(
        {
            "member_name": "Test",
            "member_id": "1",
            "enrollment_date": "2024-02-01",
            "last_flight_date": "2024-01-01",
        }
    )
    assert any(e["check"] == "DATE_CONSISTENCY" for e in errors)
