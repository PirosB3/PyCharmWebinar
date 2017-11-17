import typing
from collections import defaultdict, deque, namedtuple
from enum import Enum
from typing import Dict, TypeVar, Generic, Iterator, cast, Optional, List

from typing_extensions import Protocol


PyTodoItem = namedtuple('PyTodoItem', ['title', 'priority', 'owners', 'category'])


class Priority(Enum):
    LOW = 1
    MED = 2
    HIGH = 3


class PriorityLinkedList(object):
    """A Linked List arranged by priority

    For every type of priority (HIGH, MED, LOW) create a list
    where TodoItems are stored. Retreive the top K ordered by
    priority and time inserted (FIFO)
    """

    def __init__(self) -> None:
        self.queues: Dict[Priority, List[PriorityLinkedList]] = defaultdict(list)
        self.count = 0

    def add_item(self, item):
        """Adds a TodoItem item in the priority Linked List

        :param item: a TodoItem
        """
        self.queues[item.priority].append(item)
        self.count += 1

    def get_top(self, k=None):
        """Returns the top K results from the linked list, sorted by priority and time

        :param k: an integer specifying how many items we want back, or None if we want them all
        :return: a generator that will generate K TodoItems
        """
        if k is None:
            to_yield = float('inf')
        else:
            to_yield = k
        for priority in [Priority.HIGH, Priority.MED, Priority.LOW]:
            for item in self.queues[priority]:
                yield item
                to_yield -= 1
                if to_yield == 0:
                    break

    def remove_item(self, item):
        """Removes an item from the linked list

        :param item: the TodoItem
        """
        self.queues[item.priority].remove(item)
        self.count -= 1
