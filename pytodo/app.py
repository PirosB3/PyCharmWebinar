from collections import namedtuple


from pytodo.utils import PriorityLinkedList, Priority


PyTodoItem = namedtuple('PyTodoItem', 'title priority owners category')


class PyCategory(object):

    def __init__(self, name):
        self.items = PriorityLinkedList()
        self.name = name

    def mark_complete(self, item) -> None:
        self.items.remove_item(item)

    @property
    def authors(self):
        all_authors = set()
        for item in self.items.get_top():
            all_authors.update(item.owners)
        return all_authors

    def get_first(self):
        result = list(self.items.get_top(1))
        return None if len(result) == 0 else result[0]

    def add_todo(self, title, owner, priority) -> PyTodoItem:

        if isinstance(owner, str):
            owner = [owner]

        new_item = PyTodoItem(
            title=title,
            priority=priority,
            owners=list(owner),
            category=self.name,
        )
        self.items.add_item(new_item)
        return new_item


class PyTodo(object):

    def __init__(self):
        self.categories = {}

    @property
    def num_items(self):
        return sum(category.items.count for category in self.categories.values())

    @property
    def num_categories(self):
        return len(set(self.categories))

    def mark_complete(self, todo_item):
        self.get_category(todo_item.category).mark_complete(todo_item)

    def get_category(self, category_name):
        try:
            return self.categories[category_name]
        except KeyError:
            new_category = PyCategory(category_name)
            self.categories[category_name] = new_category
            return new_category

    @property
    def authors(self):
        result = set()
        for category in self.categories.values():
            result |= category.authors
        return result

    def get_top(self, k):
        results = []
        for category in self.categories.values():
            for item in category.items.get_top(k):
                results.append((-item.priority.value, item.category, item))
        results.sort()
        return (item for _, _, item in results[:k])
