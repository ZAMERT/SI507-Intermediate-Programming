from linked_list import LinkedList
from typing import Any

class Stack:
    """
    A stack implementation using a linked list.
    
    The stack is a LIFO (Last In, First Out) data structure.
    """

    def __init__(self) -> None:
        """
        Initialize a new Stack instance.
        """
        self.list = LinkedList()

    def push(self, data) -> None:
        """
        Add an element to the top of the stack.

        Parameters
        ----------
        data : Any
            The data to be added to the stack.
        """
        self.list.append(data)

    def pop(self) -> Any | None:
        """
        Remove and return the top element of the stack.

        Returns
        -------
        Any or None
            The data from the top of the stack, or None if the stack is empty.
        """
        return self.list.pop()

    def peek(self) -> Any | None:
        """
        Return the top element of the stack without removing it.

        Returns
        -------
        Any or None
            The data from the top of the stack, or None if the stack is empty.
        """
        return self.list.getBack()

    def isEmpty(self) -> bool:
        """
        Check if the stack is empty.

        Returns
        -------
        bool
            True if the stack is empty, False otherwise.
        """
        return (self.list.getSize() == 0)


if __name__ == "__main__":
    pass