from typing import Union, Dict, Optional, List, Set, NamedTuple, Iterator
from enum import Enum

import itertools

from pytodo.utils import PriorityLinkedList, Priority


class PyTodoItem(NamedTuple):
    title: str
    priority: Priority
    owners: List[str]
    category: str


class PyCategory(object):

    def __init__(self, name) -> None:
        self.items: PriorityLinkedList[PyTodoItem] = PriorityLinkedList()
        self.name = name

    def mark_complete(self, item: PyTodoItem) -> None:
        self.items.remove_item(item)

    @property
    def authors(self) -> Set[str]:
        all_authors: Set[str] = set()
        for item in self.items.get_top():
            all_authors.update(item.owners)
        return all_authors

    def get_last(self) -> Optional[PyTodoItem]:
        result = list(self.items.get_top(1))
        return None if len(result) == 0 else result[0]

    def add_todo(self, title: str, owner: Union[str, List[str]], priority: Priority = Priority.MED) -> PyTodoItem:

        if isinstance(owner, str):
            owner = [owner]

        new_item = PyTodoItem(
            title=title,
            priority=priority,
            owners=owner,
            category=self.name,
        )
        self.items.add_item(new_item)
        return new_item


class PyTodo(object):

    def __init__(self) -> None:
        self.categories: Dict[str, PyCategory] = {}

    @property
    def num_items(self) -> int:
        return sum(category.items.count for category in self.categories.values())

    @property
    def num_categories(self) -> int:
        return len(set(self.categories))

    def mark_complete(self, todo_item: PyTodoItem) -> None:
        self.get_category(todo_item.category).mark_complete(todo_item)

    def get_category(self, category_name: str) -> PyCategory:
        try:
            return self.categories[category_name]
        except KeyError:
            new_category = PyCategory(category_name)
            self.categories[category_name] = new_category
            return new_category

    @property
    def authors(self) -> Set[str]:
        result: Set[str] = set()
        for category in self.categories.values():
            result |= category.authors
        return result

    def get_top(self, k: int) -> Iterator[PyTodoItem]:
        results = []
        for category in self.categories.values():
            for item in category.items.get_top(k):
                results.append((-item.priority.value, item.category, item))
        results.sort()
        return (item for _, _, item in results[:k])
