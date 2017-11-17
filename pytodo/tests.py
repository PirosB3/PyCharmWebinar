import unittest

from pytodo.app import PyTodo, Priority, PyTodoItem
from pytodo.utils import PriorityLinkedList


class PriorityLinkedListTestCase(unittest.TestCase):

    def test_it_works(self):
        world_item = PyTodoItem(title="World", priority=Priority.MED, owners=[], category='')
        hello_item = PyTodoItem(title="Hello", priority=Priority.HIGH, owners=[], category='')
        sweet_item = PyTodoItem(title="Sweet", priority=Priority.HIGH, owners=[], category='')

        ll = PriorityLinkedList()
        ll.add_item(world_item)
        ll.add_item(hello_item)
        ll.add_item(sweet_item)
        self.assertEqual([item.title for item in ll.get_top(3)], ["Hello", "Sweet", "World"])

        ll.remove_item(hello_item)
        self.assertEqual([item.title for item in ll.get_top(3)], ["Sweet", "World"])


class TodoAppTestCase(unittest.TestCase):

    def test_new_todo_list(self):
        a_list = PyTodo()
        self.assertEqual(a_list.num_categories, 0)
        self.assertEqual(a_list.num_items, 0)

    def test_get_category(self):
        a_list = PyTodo()
        category_lorem = a_list.get_category('lorem')
        category_ipsum = a_list.get_category('ipsum')

        self.assertNotEqual(category_ipsum, category_lorem)
        self.assertEqual(category_lorem, a_list.get_category('lorem'))
        self.assertEqual(a_list.num_categories, 2)
        self.assertEqual(a_list.num_items, 0)

    def test_add_item_to_category(self):
        a_list = PyTodo()
        first_todo = a_list.get_category("friends").add_todo("buy present for Paul Everitt", owner="Daniel",
                                                          priority=Priority.MED)
        second_todo = a_list.get_category("work").add_todo("finish balance sheet", owner=['Daniel', 'David'],
                                                           priority=Priority.HIGH)
        self.assertEqual(a_list.num_items, 2)
        self.assertEqual(a_list.authors, {'Daniel', 'David'})

        a_list.mark_complete(second_todo)
        self.assertEqual(a_list.num_items, 1)
        self.assertEqual(a_list.authors, {'Daniel'})

        a_list.get_category("friends").mark_complete(first_todo)
        self.assertEqual(a_list.num_items, 0)
        self.assertEqual(a_list.authors, set())

    def test_get_last_added_item(self):
        a_list = PyTodo()
        my_category = a_list.get_category("friends")
        self.assertIsNone(my_category.get_first())

        my_category.add_todo("hello world", owner="Daniel")
        last = my_category.get_first()
        assert last
        self.assertEqual(last.title, "hello world")

    def test_get_top_k(self):
        a_list = PyTodo()
        a_list.get_category("home").add_todo("P3", "daniel", Priority.LOW)
        a_list.get_category("home").add_todo("P2-1", "adam", Priority.MED)
        a_list.get_category("work").add_todo("P2-2", "daniel", Priority.MED)
        a_list.get_category("leisure").add_todo("P1", "sam", Priority.HIGH)
        res = a_list.get_top(3)
        self.assertEqual([item.title for item in res], ['P1', 'P2-1', 'P2-2'])


if __name__ == '__main__':
    unittest.main()
