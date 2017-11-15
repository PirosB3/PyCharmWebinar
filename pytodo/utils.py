import typing
from collections import defaultdict, deque
from enum import Enum
from typing import Dict, TypeVar, Generic, Iterator, cast, Optional

from typing_extensions import Protocol


class Priority(Enum):
    LOW = 1
    MED = 2
    HIGH = 3


T = TypeVar('T', covariant=True)


class Prioritizable(Protocol[T]):
    priority: Priority


class PriorityLinkedList(Generic[T]):

    def __init__(self) -> None:
        self.queues: Dict[Priority, typing.Deque[Prioritizable[T]]] = defaultdict(deque)
        self.count = 0

    def add_item(self, item: Prioritizable[T]) -> None:
        self.queues[item.priority].append(item)
        self.count += 1

    def get_top(self, k: Optional[int] = None) -> Iterator[T]:
        if k is None:
            to_yield = float('inf')
        else:
            to_yield = k
        for priority in [Priority.HIGH, Priority.MED, Priority.LOW]:
            for item in self.queues[priority]:
                yield cast(T, item)
                to_yield -= 1
                if to_yield == 0:
                    break

    def remove_item(self, hello_item: Prioritizable[T]) -> None:
        self.queues[hello_item.priority].remove(hello_item)
        self.count -= 1
