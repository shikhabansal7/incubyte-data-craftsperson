from datetime import date
import pytest

@pytest.fixture
def reference_date():
    return date(2024, 1, 15)
