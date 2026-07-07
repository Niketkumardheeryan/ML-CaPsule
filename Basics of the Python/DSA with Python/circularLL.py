class Node:
    def __init__(self, data):
        self.data = data 
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None 

    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data)
            cur=cur.next
            if cur == self.head:
                break
    
    def append(self, data):

	# No intial nodes condition
        if not self.head:
            self.head = Node(data)
            self.head.next = self.head

	# nodes are there already condition
        else:
            new_node = Node(data)
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            cur.next = new_node
            new_node.next = self.head



    def prepend(self, data):

        new_node = Node(data)
        cur = self.head 
        # point the next to intial first node
        new_node.next = self.head


        # NO INTIAL NODES CONDITION
        if not self.head:
            new_node.next = new_node

        # NODES ALREADY EXISTS CONDITION
        else:
            while cur.next != self.head:
                cur = cur.next
            cur.next = new_node
        self.head = new_node



    
    def __len__(self):
        count=1
        cur = self.head
        while cur:
            count+=1
            cur=cur.next
            if cur == self.head:
                break
            return count


    def split_list(self):
        size = len(self)    

        if size == 0:
            return None
        if size == 1:
            return self.head

        mid = size//2
        count = 0

        prev = None
        cur = self.head

        # first list code
        while cur and count < mid:
            count += 1
            prev = cur
            cur = cur.next
        prev.next = self.head 
        # first list done

        
        # second list code
        split_cllist = CircularLinkedList()
        while cur.next != self.head:
            split_cllist.append(cur.data)
            cur = cur.next
        split_cllist.append(cur.data)
        # second list done


