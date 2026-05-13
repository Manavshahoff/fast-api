import pytest
from app.calculations import BankAccount

@pytest.fixture
def zero_bank_account():
    bank_account = BankAccount(50.0)
    return bank_account

@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (50.0, 25.0, 75.0),
    (100.0, 50.0, 100.0),
    (200.0, 150.0, 100.0)
])
def test_bank_transaction(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.get_balance() == expected


def test_insufficient_funds(zero_bank_account):
    with pytest.raises(ValueError):
        zero_bank_account.withdraw(100.0)