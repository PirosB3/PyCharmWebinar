from typing import Tuple, Dict, Optional, List

SpendResult = Tuple[bool, int]


def add_two_numbers(num_a: int, num_b: int) -> int:
    a = num_a + num_b
    return a


class Bank(object):

    def __init__(self) -> None:
        self.name_to_customer_map: Dict[str, 'Customer'] = {}

    def add_customers(self, *customers: 'Customer') -> List[bool]:
        results = []
        for customer in customers:
            if customer.name in self.name_to_customer_map:
                results.append(False)
            self.name_to_customer_map[customer.name] = customer
            results.append(True)
        return results

    def transfer_funds(self, customer_a_name: str, customer_b_name: str, amount: int) -> bool:
        if amount <= 0:
            return False

        try:
            customer_a = self.name_to_customer_map[customer_a_name]
            customer_b = self.name_to_customer_map[customer_b_name]
        except KeyError:
            return False

        customer_a_acct = customer_a.primary_account
        customer_b_acct = customer_b.primary_account
        if not customer_a_acct or not customer_b_acct:
            return False

        if not customer_a_acct.spend(amount)[0]:
            return False

        return customer_b_acct.credit(amount)


class Customer(object):

    def __init__(self, name: str) -> None:
        self.name = name
        self.accounts: List[Account] = []
        self.primary_account_name: Optional[str] = None

    def add_account(self, account: 'Account', is_primary: bool = False) -> None:
        self.accounts.append(account)
        if is_primary:
            self.primary_account_name = account.name

    @property
    def primary_account(self) -> Optional['Account']:
        if self.primary_account_name is None:
            return None
        return self.find_account(self.primary_account_name)

    def find_account(self, name: str) -> Optional['Account']:
        for account in self.accounts:
            if account.name == name:
                return account
        return None

    def spend_primary_account(self, amount: int) -> bool:
        primary_account = self.primary_account
        if primary_account is None:
            return False

        succeeded, amount_remaining = primary_account.spend(amount)
        return succeeded

    def credit_primary_account(self, amount: int) -> bool:
        if self.primary_account_name is None:
            return False

        account = self.find_account(self.primary_account_name)
        if account is None:
            return False
        account.credit(amount)
        return True


class Account(object):
    def __init__(self, name: str, initial_balance: int) -> None:
        self.name = name
        self.balance = initial_balance

    def credit(self, amount: int) -> bool:
        if amount < 0:
            return False
        self.balance = add_two_numbers(self.balance, amount)
        return True

    def spend(self, amount: int) -> SpendResult:
        if amount < 0:
            return False, self.balance

        if amount > self.balance:
            return False, self.balance

        self.balance -= amount
        return True, self.balance


def main() -> None:
    result = add_two_numbers(2, 5)

    bank = Bank()

    c1 = Customer("Daniel")
    c1.add_account(Account("checking", 300), True)

    c2 = Customer("Paul")
    c2.add_account(Account("checking", 500), True)

    bank.add_customers(c1, c2)
    for _ in range(10):
        print(bank.transfer_funds("Paul", "Daniel", 100))

if __name__ == '__main__':
    main()
