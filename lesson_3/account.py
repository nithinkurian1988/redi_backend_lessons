class Account:

    def __init__(self, account_number: str, pin_code: int, initial_balance: float = 0.0) -> None:
        self.account_number = account_number
        self.pin_code = pin_code
        self.balance = initial_balance

    def deposit(self, account_number: str, pin_code: int, amount: float) -> None:
        # verify both account number and pin code before making a transaction
        if self.account_number != account_number:
            raise ValueError("Invalid account number.")
        if not isinstance(pin_code, int):
            raise TypeError("Pin code must be an integer.")
        if self.pin_code != pin_code:
            raise ValueError("Invalid pin code.")  
         
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        self.balance += amount

    def withdraw(self, account_number: str, pin_code: int, amount: float) -> None:
        # verify both account number and pin code before making a transaction
        if self.account_number != account_number:
            raise ValueError("Invalid account number.")
        if not isinstance(pin_code, int):
            raise TypeError("Pin code must be an integer.")
        if self.pin_code != pin_code:
            raise ValueError("Invalid pin code.")  

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self) -> float:
        return self.balance
