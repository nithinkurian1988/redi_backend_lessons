import pytest

from .currency_converter import CurrencyConverter

@pytest.fixture
def currency_converter():
    return CurrencyConverter()

def test_conversion_valid(currency_converter):
    assert currency_converter.convert("EUR", "USD", 50.5) == 50.5 * 1.09
    assert currency_converter.convert("USD", "EUR", 100) == 100 * 0.92
    assert currency_converter.convert("EUR", "JPY", 5) == 5 * 130.0
    assert currency_converter.convert("USD", "GBP", 20) == 20 * 0.75

def test_conversion_unsupported_pair(currency_converter):
    with pytest.raises(ValueError):
        currency_converter.convert("USD", "INR", 10)
    with pytest.raises(ValueError):
        currency_converter.convert("AUD", "EUR", 10)
    with pytest.raises(ValueError):
        currency_converter.convert("AUD", "USD", 10)
    with pytest.raises(ValueError):
        currency_converter.convert("INR", "INR", 10)

def test_conversion_invalid_amount(currency_converter):
    with pytest.raises(TypeError):
        currency_converter.convert("EUR", "USD", "50")

def test_conversion_negative_amount(currency_converter):
    with pytest.raises(ValueError):
        currency_converter.convert("EUR", "USD", -5)

def test_conversion_invalid_currency_code_type(currency_converter):
    with pytest.raises(TypeError):
        currency_converter.convert(123, "USD", 10)
    with pytest.raises(TypeError):
        currency_converter.convert("EUR", 456, 10)
    with pytest.raises(TypeError):
        currency_converter.convert(123, 456, 10)

def test_conversion_invalid_currency_code_length(currency_converter):
    with pytest.raises(ValueError):
        currency_converter.convert("EURO", "USD", 10)
    with pytest.raises(ValueError):
        currency_converter.convert("EUR", "US", 10)
    with pytest.raises(ValueError):
        currency_converter.convert("E", "USD", 10)
    with pytest.raises(ValueError):
        currency_converter.convert("EUR", "USDA", 10)

def test_conversion_case_insensitivity(currency_converter):
    assert currency_converter.convert("eur", "usd", 10) == 10 * 1.09
    assert currency_converter.convert("Usd", "eUr", 20) == 20 * 0.92
    assert currency_converter.convert("jPy", "gBp", 15) == 15 * 0.0068
    assert currency_converter.convert("gBp", "jPy", 30) == 30 * 150.0

def test_conversion_zero_amount(currency_converter):
    assert currency_converter.convert("EUR", "USD", 0) == 0
    assert currency_converter.convert("USD", "GBP", 0) == 0
    assert currency_converter.convert("JPY", "EUR", 0) == 0
    assert currency_converter.convert("GBP", "JPY", 0) == 0

def test_conversion_int_amount(currency_converter):
    assert currency_converter.convert("EUR", "USD", 10) == 10 * 1.09
    assert currency_converter.convert("USD", "EUR", 50) == 50 * 0.92
    assert currency_converter.convert("JPY", "GBP", 1000) == 1000 * 0.0068
    assert currency_converter.convert("GBP", "JPY", 200) == 200 * 150.0

def test_conversion_large_amount(currency_converter):
    assert currency_converter.convert("EUR", "USD", 1_000_000) == 1_000_000 * 1.09
    assert currency_converter.convert("USD", "EUR", 5_000_000) == 5_000_000 * 0.92
    assert currency_converter.convert("JPY", "GBP", 10_000_000) == 10_000_000 * 0.0068
    assert currency_converter.convert("GBP", "JPY", 2_000_000) == 2_000_000 * 150.0



