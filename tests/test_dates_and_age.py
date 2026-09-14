from datetime import date

from src_logic import calculate_age, parse_compact_date, is_stale


def test_parse_yyyymmdd():
    assert parse_compact_date("20101012", "YYYYMMDD") == date(2010, 10, 12)


def test_invalid_month_returns_none():
    assert parse_compact_date("20211313", "YYYYMMDD") is None


def test_parse_mmddyyyy():
    assert parse_compact_date("03051985", "MMDDYYYY") == date(1985, 3, 5)


def test_age_is_birthday_aware():
    assert calculate_age(date(2000, 1, 16), date(2024, 1, 15)) == 23
    assert calculate_age(date(2000, 1, 15), date(2024, 1, 15)) == 24


def test_missing_dob_produces_no_age():
    assert calculate_age(None, date(2024, 1, 15)) is None


def test_stale_member_over_90_days():
    assert is_stale(date(2023, 10, 16), date(2024, 1, 15)) is True
    assert is_stale(date(2023, 10, 17), date(2024, 1, 15)) is False
    assert is_stale(None, date(2024, 1, 15)) is False
