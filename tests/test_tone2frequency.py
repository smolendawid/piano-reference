import pytest

from core.tone2frequency import tone2frequency


def test_tone2frequency():
    assert pytest.approx(round(tone2frequency(40), 2)) == 261.52
