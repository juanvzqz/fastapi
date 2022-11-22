from app.calculations import add, BankAccount, InsufficientFunds
import pytest
# py -3 tests/test_calculations.py
# naming matters should be test_XXXXX

# pytest --help
# pytest -v for verbosity
# -s to keep the "print" statements
# -r show extra chars
# pytest --disable-warnings TO DISABLE ALL UNUSEFUL WARNINGS
# -x TO STOP THE TEST IF ANYONE FAILS


@pytest.fixture()
def zero_bank_account():
    print('---->>>>creating empty bank account')
    return BankAccount()


@pytest.fixture()
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    # print('Testing add function')
    assert add(num1, num2) == expected


def test_bank_set_initial_amount(bank_account):
    # it calls the fixture bank_account and stores the return in a variable with the same name
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    # it calls the fixture zero_bank_account and stores the return in a variable with the same name
    print('---->>>>testing my bank account')
    assert zero_bank_account.balance == 0


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_bank_transactions(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    # To indicate that an error is expected.
    # The Exception expected must be provided
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
