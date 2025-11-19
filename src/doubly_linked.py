class Node:
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.header = None
        self.tail = None

    def __repr__(self):
        string = "<"
        current = self.header
        while current:
            string += str(current.item)
            if current.next:
                string += ", "
            current = current.next
        return string + ">"

    def add_front(self, new_item):
        added_node = Node(new_item)
        if self.header is None:
            self.header = added_node
            self.tail = added_node
        else:
            added_node.next = self.header
            self.header.prev = added_node
            self.header = added_node

    def add_back(self, new_item):
        added_node = Node(new_item)
        if self.header is None:
            self.header = added_node
            self.tail = added_node
        else:
            self.tail.next = added_node
            added_node.prev = self.tail
            self.tail = added_node

    def remove_front(self):
        if self.header is None:
            return None
        removed_node = self.header.item
        self.header = self.header.next
        if self.header is None:
            self.tail = None
        else:
            self.header.prev = None
        return removed_node

    def remove_back(self):
        if self.tail is None:
            return None
        removed_node = self.tail.item
        self.tail = self.tail.prev
        if self.tail is None:
            self.header = None
        else:
            self.tail.next = None
        return removed_node

    def concatenate(self, other):
        if self.header is None:
            new_node = other.header
            new_node.prev = None
            self.header = new_node
        else:
            new_node = other.header
            current = self.header
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current
            new_node.next = other.header.next