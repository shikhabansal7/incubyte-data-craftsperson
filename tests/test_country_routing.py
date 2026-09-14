from src_logic import latest_records_by_member, route_country


def test_country_normalization():
    assert route_country("IND") == "INDIA"
    assert route_country("india") == "INDIA"
    assert route_country("USA") == "USA"
    assert route_country("AU") == "AUS"
    assert route_country(None) == "OTHER"


def test_latest_record_wins_for_member_movement():
    records = [
        {"member_id": "223457", "country": "USA", "ingested_at": 1},
        {"member_id": "223457", "country": "IND", "ingested_at": 2},
        {"member_id": "223458", "country": "USA", "ingested_at": 3},
    ]

    current = latest_records_by_member(records)

    assert current["223457"]["country"] == "IND"
    assert current["223458"]["country"] == "USA"


def test_latest_record_does_not_duplicate_old_country():
    records = [
        {"member_id": "1", "country": "USA", "ingested_at": 10},
        {"member_id": "1", "country": "IND", "ingested_at": 20},
    ]

    current = latest_records_by_member(records)
    routed = {route_country(row["country"]) for row in current.values()}

    assert routed == {"INDIA"}
