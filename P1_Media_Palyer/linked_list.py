from typing import Any

class Node:
    """
    A node in a doubly linked list.

    Attributes
    ----------
    data : Any
        The data stored in the node.
    next : Node or None
        The next node in the linked list.
    prev : Node or None
        The previous node in the linked list.

    Parameters
    ----------
    data : Any, optional
        The data to be stored in the node (default is None).
    """
    
    def __init__(self, data = None) -> None:
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:
    """
    A doubly linked list with dummy head and tail nodes to simplify node insertion and deletion.
    We require using dummyHead and dummyTail, since it will make certain implementation easier.
    Notice, the linked list is zero indexed.  

    Attributes
    ----------
    dummyHead : Node
        A dummy head node of the linked list.
    dummyTail : Node
        A dummy tail node of the linked list.
    size : int
        The number of elements in the linked list.

    Methods
    -------
    get(index)
        Retrieves the data at the specified index in the linked list.

    appendLeft(data)
        Adds a node with the given data at the beginning of the linked list.

    append(data)
        Adds a node with the given data at the end of the linked list.

    popLeft()
        Removes and returns the data from the beginning of the linked list.

    pop()
        Removes and returns the data from the end of the linked list.

    addAtIndex(index, data)
        Adds a node with the given data at the specified index in the linked list.

    deleteAtIndex(index)
        Deletes the node at the specified index from the linked list.

    printFromFront()
        Prints all elements of the linked list from front to back.

    printFromBack()
        Prints all elements of the linked list from back to front.

    _isNodeUnbound(node)
        Checks if the given node's linkage in the list is broken. 
        More specifically, check if the node is removed.

    getFront()
        Returns the data from the front (head) of the linked list.

    getBack()
        Returns the data from the back (tail) of the linked list.

    getSize()
        Returns the number of elements in the linked list.
    """

    def __init__(self) -> None:
        """
        Initializes a LinkedList instance with dummy head and tail nodes and sets size to zero.
        Notice data attribute of the dummyHead and dummyTail is None
        """
        self.dummyHead = Node(None)
        self.dummyTail = Node(None)
        self.dummyHead.next = self.dummyTail
        self.dummyTail.prev = self.dummyHead
        self.size = 0
        
    def _getNode(self,index: int) -> Node | None:
        """
        Help function to return a node at index i. 
        If the index is invalid, return Node. 

        Parameters
        ----------
        index : int
            The index of the node whose data is to be retrieved.

        Returns
        -------
        Node or None
            The node at the specified index or None if index is invalid.
        """
        # Check if the index is within the range.
        if index < 0 or index >= self.size:
            return None
        
        curr = self.dummyHead.next
        for _ in range(index):
            curr = curr.next
            
        return curr
    
    def get(self ,index: int) -> Any | None:
        """
        Retrieve the data at the specified index in the linked list.
        If the index is invalid, ie out of range, return None.


        Parameters
        ----------
        index : int
            The index of the node whose data is to be retrieved.

        Returns
        -------
        any or None
            The data at the specified index or None if index is invalid.
        """
        indexNode = self._getNode(index)
        return indexNode.data if indexNode else None


    def appendLeft(self, data) -> None:
        """
        Create a new node, and assign the data to the new node.
        Add the node with the given data at the beginning of the linked list.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.
        Increment the size by one.

        Parameters
        ----------
        data : any
            The data to be stored in the new node.

        Returns
        -------
        None
        """
        # Create a new node. 
        newNode = Node(data)
        firstNode = self.dummyHead.next
        
        # Change pointer. 
        self.dummyHead.next = newNode
        newNode.prev = self.dummyHead
        newNode.next = firstNode
        firstNode.prev = newNode
        
        # Add size. 
        self.size += 1


    def append(self, data) -> None:
        """
        Add a node with the given data at the end of the linked list.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.
        Increment the size by one.

        Parameters
        ----------
        data : any
            The data to be stored in the new node.

        Returns
        -------
        None
        """
        # Create a new Node.
        newNode = Node(data)
        lastNode = self.dummyTail.prev
        
        # Modify pointers.
        newNode.next = self.dummyTail
        newNode.prev = lastNode
        lastNode.next = newNode
        self.dummyTail.prev = newNode
        
        # Add size.
        self.size += 1

    
    def popLeft(self) -> Any | None:
        """
        Remove and return the data from the beginning of the linked list.
        Decrease the size by one.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.

        Returns
        -------
        any
            The data of the removed node, or None if the list is empty.

        None 
            If the linked list is empty.
        """
        # Return None of the list is empty.
        if self.size == 0:
            return None
        
        # Extract first node's data
        firstNode = self.dummyHead.next
        data = firstNode.data
        
        # Change pointer.
        self.dummyHead.next = firstNode.next
        firstNode.next.prev = self.dummyHead
        
        # Change size.
        self.size -= 1
        
        return data


    def pop(self) -> Any | None:
        """
        Remove and return the data from the end of the linked list.
        Decrease the size by one.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.

        Returns
        -------
        any
            The data of the removed node, or None if the list is empty.
        None 
            If the linked list is empty.
        """
        # Return None of the list is empty.
        if self.size == 0:
            return None
        
        # Extract last node's data
        lastNode = self.dummyTail.prev
        data = lastNode.data
        
        # Change pointer.
        self.dummyTail.prev = lastNode.prev
        lastNode.prev.next = self.dummyTail
        
        # Change size.
        self.size -= 1
        
        return data
            

    def addAtIndex(self, index: int, data: int) -> bool:
        """
        Add a node with the given data at the specified index in the linked list.
        You could assume the only illegal input is an out of range index. 
        Notice, you need to reset the connection at both side. 

        Parameters
        ----------
        index : int
            The index at which the new node should be inserted.
        data : any
            The data to be stored in the new node.

        Returns
        -------
        bool
            True if the addition was successful, False otherwise.
        """
        # Check whether index is within the range.
        if index < 0 or index > self.size:
            return False
        
        if index == 0:
            self.appendLeft(data)
            return True
        if index == self.size:
            self.append(data)
            return True
        
        # Insert in the list.
        newNode = Node(data)
        nextNode = self._getNode(index) # The original node at index will be postponed by 1.
        if not nextNode:
            return False
        prevNode = nextNode.prev
        
        # Modify pointer.
        newNode.prev = prevNode
        newNode.next = nextNode
        prevNode.next = newNode
        nextNode.prev = newNode
        self.size += 1
        
        return True


    def deleteAtIndex(self, index: int) -> bool:
        """
        Delete a node with the given data at the specified index in the linked list.
        You could assume the only illegal input is an out of range index. 
        Notice, you need to reset the connection at both side. 

        Parameters
        ----------
        index : int
            The index at which the new node should be inserted.

        Returns
        -------
        bool
            True if the addition was successful, False otherwise.
        """
        # Check whether index is within the range.
        if index < 0 or index >= self.size:
            return False
        
        if index == 0:
            self.popLeft()
            return True
        if index == (self.size-1):
            self.pop()
            return True
        
        delNode = self._getNode(index)
        delNode.prev.next = delNode.next
        delNode.next.prev = delNode.prev
        self.size -= 1
        
        return True


    def printFromFront(self) -> None:
        """
        Print all elements of the linked list from front to back,
        each element should be in a separate line. 
        If the linked list is empty, print exactly this string "Link list is empty."
        You should not include the value of dummy head or tail.

        Expected Output:
        firstElement  
        secondElement 
        ...
        """
        if self.size == 0:
            print("Link list is empty.")
            return
        curr = self.dummyHead.next
        while curr != self.dummyTail:
            print(curr.data)
            curr = curr.next
            
        return


    def printFromBack(self) -> None:
        """
        Prints all elements of the linked list from back to front.
        If the linked list is empty, print exactly this string "Link list is empty."
        Follow the same format of printFromFront()
        """
        if self.size == 0:
            print("Link list is empty.")
            return
        
        curr = self.dummyTail.prev
        while curr != self.dummyHead:
            print(curr.data)
            curr = curr.prev
        
        return


    def _isNodeUnbound(self,node) -> bool:
        """
        A private method. 
        Check if the given node's linkage in the list is broken.
        This means the node does not appear in the traversal from head to tail.
        In the other words, check if the connection relation between the node 
        and the node before it is neutral. 
        Notice this method assumes all the methods related to delete a node are 
        implemented correctly. 

        Parameters
        ----------
        node : Node
            The node to check for broken linkage.

        Returns
        -------
        bool
            True if the node's linkage is broken, False otherwise.

        Example
        --------
        check if the next attribute of the node's previous node is 
        the node.
        """
        if node is None:
            return True
        if node.prev is None:
            return True
        return node.prev.next !=node

    
    def getFront(self) -> Any | None:
        """
        Returns the data from the first non dummy node in the linked list.

        Returns
        -------
        data or None
            The data of the first node in the list, or None if the list is empty.
        """
        if self.size == 0:
            return None
        return self.dummyHead.next.data

    def getBack(self) -> Any | None:
        """
        Returns the data from the last non dummy node in the linked list.

        Returns
        -------
        data or None
            The data of the last node in the list, or None if the list is empty.
        """
        if self.size == 0:
            return None
        return self.dummyTail.prev.data
    
    def getSize(self) -> int:
        """
        Return the number of elements in the stack or queue.

        This method provides the current size of the linked list, 
        indicating how many elements are stored in it.

        Returns
        -------
        int
            The number of elements in linked list.
        """
        return self.size
        
"""
############################## Homework linked_list ##############################

% Student Name: Yuchen Liu

% Student Unique Name: ylyuchen

% Lab Section 00X: 1

% I worked with the following classmates: Nobody

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

if __name__ == "__main__":
    pass
