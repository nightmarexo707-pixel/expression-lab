"""A small, inspectable LIFO stack used by Expression Lab."""
from typing import Generic, TypeVar

T = TypeVar("T")


class StackError(IndexError):
    """Raised when an operation requires an item from an empty stack."""


class Stack(Generic[T]):
    """List-backed LIFO stack.

    push/pop/peek are O(1) amortized; is_empty and size are O(1).
    """
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Place an item on top of the stack. O(1) amortized."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item. O(1); raises StackError on underflow."""
        if self.is_empty():
            raise StackError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it. O(1)."""
        if self.is_empty():
            raise StackError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return whether the stack contains no items. O(1)."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of stored items. O(1)."""
        return len(self._items)
