class Currency_converter:
    def __init__(self):
        rates = {
            "USDEUR": 0.92,
            "EURUSD": 1.09,
            "EURJPY": 130.0,
            "USDGBP": 0.75,
            "EURAUD": 1.54 
        }
        self.rates = rates

    def conversion(self, initial_currency: str, final_currency: str, amount: float) -> float:       
        if isinstance(amount, (int, float)) is False:
            raise TypeError("Amount must be a non-negative number")
        
        if amount < 0:
            raise ValueError("Amount must be a non-negative number")

        pair = initial_currency + final_currency
        if pair in self.rates:
            rate = self.rates[pair]
            return amount * rate
        else:
            raise ValueError("Conversion rate not available")


currency_converter = Currency_converter()
print(currency_converter.conversion("EUR", "USD", 10))