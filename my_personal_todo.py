import argparse

from pytodo.app import PyTodo
from pytodo.utils import Priority


ITEMS_TO_ADD = [
    ("home", "Clean house", ["Matt", "Jay"], Priority.LOW),
    ("home", "Buy milk", "Matt", Priority.MED),
    ("home", "Do washing", "Daniel", Priority.LOW),
    ("work", "Check metrics", "Daniel", Priority.MED),
    ("work", "Fix server crashing", "Daniel", Priority.HIGH),
    ("personal", "do PyCharm webinar", ["Daniel", "Paul"], Priority.HIGH),
]


def main() -> None:
    my_list = PyTodo()

    for category, title, authors, priority in ITEMS_TO_ADD:
        my_list.get_category(category).add_todo(title, authors, priority)

    for idx, item in enumerate(my_list.get_top(5)):
        print(f"Item #{idx}: {item.title}")

    highest_priority_item = my_list.get_category("home").get_first()
    if highest_priority_item is not None:
        print(f"Highest priority item at home is: {highest_priority_item.title}")

if __name__ == '__main__':
    main()