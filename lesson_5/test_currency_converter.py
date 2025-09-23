import pytest

from .currency_converter import Currency_converter

@pytest.fixture
def currency_converter():
    return Currency_converter()

def test_conversion_valid(currency_converter):
    assert currency_converter.conversion("EUR", "USD", 50.5) == 50.5 * 1.09
    assert currency_converter.conversion("USD", "EUR", 100) == 100 * 0.92
    assert currency_converter.conversion("EUR", "JPY", 5) == 5 * 130.0
    assert currency_converter.conversion("USD", "GBP", 20) == 20 * 0.75
    assert currency_converter.conversion("EUR", "AUD", 15) == 15 * 1.54

def test_conversion_unsupported_pair(currency_converter):
    with pytest.raises(ValueError):
        currency_converter.conversion("USD", "INR", 10)
    with pytest.raises(ValueError):
        currency_converter.conversion("GBP", "EUR", 10)
    with pytest.raises(ValueError):
        currency_converter.conversion("JPY", "USD", 10)

def test_conversion_invalid_amount(currency_converter):
    with pytest.raises(TypeError):
        currency_converter.conversion("EUR", "USD", "50")

def test_conversion_negative_amount(currency_converter):
    with pytest.raises(ValueError):
        currency_converter.conversion("EUR", "USD", -5)

