def add(num1: int, num2: 2):
    return num1 + num2


class InsufficientFunds(Exception):
    # It's a child class from Exception class
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            # It calls the InsufficentFunds class
            raise InsufficientFunds('Insufficient funds in the account')
            # raise ZeroDivisionError (this will fail)
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
