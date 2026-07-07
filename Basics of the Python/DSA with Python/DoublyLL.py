
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data)
            cur = cur.next

    def append(self, data):
        #case for no nodes in intial DLL
        if self.head is None:
            new_node = Node(data)
            new_node.prev = None
            self.head = new_node
        else:
            new_node = Node(data)
            cur = self.head
            while cur.next:
                cur = cur.next
            # we have reached the last node 
            # now let's append
            cur.next = new_node
            new_node.prev = cur
            new_node.next = None

    
    def prepend(self, data):
        #case for no nodes in intial DLL
        if self.head is None:
            new_node = Node(data)
            new_node.prev = None 
            self.head = new_node
        else:
            new_node = Node(data)
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node
            new_node.prev = None

    def delete(self, key):
        cur = self.head
        while cur:
            if cur.data == key and cur == self.head:
                # Case 1:
                # if only one node in the list
                if not cur.next:
                    cur = None 
                    self.head = None
                    return

                # Case 2:
                # to delete first node
                else:
                    # making a new pointer nxt to next node of cur
                    nxt = cur.next
                    cur.next = None 
                    nxt.prev = None
                    cur = None
                    self.head = nxt
                    return 

            elif cur.data == key:
                # Case 3:
                # to delete middle node
                if cur.next:
                    # making a new pointer prev and nxt
                    nxt = cur.next 
                    prev = cur.prev
                    # strech next pointer to next node
                    prev.next = nxt
                    # strch prev pointer to previous node
                    nxt.prev = prev
                    cur.next = None 
                    cur.prev = None
                    cur = None
                    return

                # Case 4:
                else:
                    # to delete last node
                    prev = cur.prev 
                    prev.next = None 
                    cur.prev = None 
                    cur = None 
                    return 
            
            cur = cur.next

