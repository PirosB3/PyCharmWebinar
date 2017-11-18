from typing import Tuple, Dict, Optional

SpendResult = Tuple[bool, int]


def add_two_numbers(num_a: int, num_b: int) -> int:
    a = num_a + num_b
    return a


class Customer(object):

    def __init__(self, name) -> None:
        self.name = name
        self.name_to_account_map: Dict[str, Account] = {}
        self.primary_account_name: Optional[str] = None

    def add_account(self, account: Account, is_primary: bool = False) -> None:
        self.name_to_account_map[account.name] = account
        if is_primary:
            self.primary_account_name = account.name

    def credit(self, amount: int) -> bool:
        if self.primary_account_name is None:
            return False

        try:
            self.name_to_account_map[self.primary_account_name].credit(amount)
            return True
        except KeyError:
            return False


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

if __name__ == '__main__':
    main()
