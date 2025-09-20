import pytest

from .account import Account


@pytest.fixture
def account() -> Account:
    return Account(account_number="123456", pin_code=789, initial_balance=100.0)


def test_initial_balance(account: Account) -> None:
    assert account.get_balance() == 100.0


def test_deposit(account: Account) -> None:
    account.deposit(account.account_number, account.pin_code, 50.0)
    assert account.get_balance() == 150.0


def test_withdraw(account: Account) -> None:
    account.withdraw(account.account_number, account.pin_code, 30.0)
    assert account.get_balance() == 70.0


def test_withdraw_insufficient_funds(account: Account) -> None:
    with pytest.raises(ValueError, match="Insufficient funds."):
        account.withdraw(account.account_number, account.pin_code, 200.0)


def test_deposit_negative_amount(account: Account) -> None:
    with pytest.raises(ValueError, match="Deposit amount must be positive."):
        account.deposit(account.account_number, account.pin_code, -20.0)


def test_withdraw_negative_amount(account: Account) -> None:
    with pytest.raises(ValueError, match="Withdrawal amount must be positive."):
        account.withdraw(account.account_number, account.pin_code, -10.0)

def test_invalid_account_number(account: Account) -> None:
    with pytest.raises(ValueError, match="Invalid account number."):
        account.deposit("wrong_number", account.pin_code, 50.0)
    with pytest.raises(ValueError, match="Invalid account number."):
        account.withdraw("wrong_number", account.pin_code, 30.0)

def test_invalid_pin_code(account: Account) -> None:
    with pytest.raises(ValueError, match="Invalid pin code."):
        account.deposit(account.account_number, 999, 50.0)
    with pytest.raises(ValueError, match="Invalid pin code."):
        account.withdraw(account.account_number, 0, 30.0)

def test_non_integer_pin_code(account: Account) -> None:
    with pytest.raises(TypeError, match="Pin code must be an integer."):
        account.deposit(account.account_number, "not_an_int", 50.0)
    with pytest.raises(TypeError, match="Pin code must be an integer."):
        account.withdraw(account.account_number, 12.34, 30.0)