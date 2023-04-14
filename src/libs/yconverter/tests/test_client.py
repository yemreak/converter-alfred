from pathlib import Path

from pytest import fixture, raises

from ..client import YConverter


@fixture
def client():
    return YConverter(Path(".key").read_text().strip())


def test_convert(client: YConverter):
    result1 = client.convert(1, "USD", "PHP")
    result2 = client.convert(1, "PHP", "USD")
    assert round(result1, 8) == round(1 / result2, 8)

    result1 = client.convert(1, "USD", "TRY")
    result2 = client.convert(1, "TRY", "USD")
    assert round(result1, 8) == round(1 / result2, 8)

    result1 = client.convert(1, "try", "usd")
    result2 = client.convert(1, "usd", "try")
    assert round(result1, 8) == round(1 / result2, 8)

    result1 = client.convert(1, "try", "usdt")
    result2 = client.convert(1, "usdt", "try")
    assert round(result1, 8) == round(1 / result2, 8)

    result1 = client.convert(1, "try", "btc")
    result2 = client.convert(1, "btc", "try")
    assert round(result1, 8) == round(1 / result2, 8)

    result1 = client.convert(1, "eur", "try")
    result2 = client.convert(1, "try", "eur")
    assert round(result1, 8) == round(1 / result2, 8)

    with raises(ValueError):
        client.convert(1, "US", "TRY")

    assert client.convert(1550000, "try", "usd")
