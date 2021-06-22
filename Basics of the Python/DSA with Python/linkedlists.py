class Node():
    def __init__(self,data=None,next=None):
        self.data=data
        self.next=next

class LL():
    def __init__(self):
        self.head=None 

	def printList(self): 
		temp = self.head 
		while (temp): 
			print temp.data, 
			temp = temp.next

    
	def push(self, new_data): 
		new_node = Node(new_data) 
		new_node.next = self.head 
		self.head = new_node 


	def insertAfter(self, prev_node, new_data): 
		if prev_node is None: 
			print "The given previous node must inLinkedList."
			return
		new_node = Node(new_data) 
		new_node.next = prev_node.next
		prev_node.next = new_node 
 
	def append(self, new_data): 
		new_node =Node(new_data)
		if self.head is None: 
			self.head = new_node 
			return
		last = self.head 
		while (last.next): 
			last = last.next
		last.next = new_node 


    def delete_node_at_pos(self, pos):

        cur_node = self.head
        
        prev = None
        count = 0
        while cur_node and count != pos:
            prev = cur_node 
            cur_node = cur_node.next
            count += 1

        if cur_node is None:
            return 

        prev.next = cur_node.next
        cur_node = None