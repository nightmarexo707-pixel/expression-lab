import unittest
from stack import Stack, StackError

class StackTests(unittest.TestCase):
    def test_empty_stack(self):
        stack = Stack()
        self.assertTrue(stack.is_empty())
        self.assertEqual(stack.size(), 0)

    def test_push_pop_and_size(self):
        stack = Stack()
        stack.push(10); stack.push(20)
        self.assertEqual(stack.size(), 2)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack.size(), 1)
        self.assertEqual(stack.pop(), 10)
        self.assertTrue(stack.is_empty())

    def test_peek_does_not_remove(self):
        stack = Stack(); stack.push("top")
        self.assertEqual(stack.peek(), "top")
        self.assertEqual(stack.size(), 1)

    def test_lifo_order(self):
        stack = Stack()
        for value in [1, 2, 3]: stack.push(value)
        self.assertEqual([stack.pop(), stack.pop(), stack.pop()], [3, 2, 1])

    def test_underflow(self):
        stack = Stack()
        with self.assertRaises(StackError): stack.pop()
        with self.assertRaises(StackError): stack.peek()

if __name__ == "__main__": unittest.main()
