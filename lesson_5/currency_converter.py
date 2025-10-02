class CurrencyConverter:
    """
    A simple currency converter that supports a limited set of currencies and fixed conversion rates.
    Supported currencies: USD, EUR, JPY, GBP
    """
    def __init__(self):
        # nested dictionary for better scalability
        self.rates = {
            "USD": {"EUR": 0.92, "GBP": 0.75, "JPY": 110.0},
            "EUR": {"USD": 1.09, "JPY": 130.0, "GBP": 0.82},
            "JPY": {"USD": 0.0091, "EUR": 0.0077, "GBP": 0.0068},
            "GBP": {"USD": 1.33, "EUR": 1.22, "JPY": 150.0}
        }

    def convert(self, initial_currency: str, final_currency: str, amount: float) -> float:  
        """
        Convert amount from initial_currency to final_currency using predefined rates.
        Parameters:
        - initial_currency (str): The currency code to convert from (e.g., "USD").
        - final_currency (str): The currency code to convert to (e.g., "EUR").
        - amount (float): The amount of money to convert.
        Returns:
        - float: The converted amount in the final_currency.
        """

        if not isinstance(initial_currency, str) or not isinstance(final_currency, str):
            raise TypeError("Currency codes must be strings")
        
        if len(initial_currency) != 3 or len(final_currency) != 3:
            raise ValueError("Currency codes must be 3 characters long")
        
        if initial_currency.upper() != initial_currency:
            initial_currency = initial_currency.upper()
        if final_currency.upper() != final_currency:
            final_currency = final_currency.upper()

        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number")
        
        if amount < 0:
            raise ValueError("Amount must be a non-negative number")

        if initial_currency not in self.rates or final_currency not in self.rates[initial_currency]:
            raise ValueError(f"Conversion from {initial_currency} to {final_currency} is not supported")
        
        rate = self.rates.get(initial_currency).get(final_currency)
        return amount * rate

# Example usage
currency_converter = CurrencyConverter()
print(currency_converter.convert("EUR", "USD", 10))