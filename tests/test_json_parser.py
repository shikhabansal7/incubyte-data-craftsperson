import json
from pathlib import Path

from src_logic import flatten_redemptions


def test_flatten_assessment_json():
    payload = json.loads(
        Path(__file__).parents[1].joinpath("data", "redemption.json").read_text()
    )

    rows = flatten_redemptions(payload)

    assert len(rows) == 2
    assert rows[0]["member_id"] == "223457"
    assert rows[0]["txn_id"] == "RX10091"
    assert rows[0]["miles_redeemed"] == 12000
    assert rows[1]["status"] == "PENDING"


def test_empty_redemptions():
    payload = {"member_id": "1", "feed_date": "20240115", "redemptions": []}
    assert flatten_redemptions(payload) == []
