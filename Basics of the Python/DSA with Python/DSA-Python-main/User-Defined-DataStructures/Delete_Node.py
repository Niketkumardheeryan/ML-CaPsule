def DeleteLast(head):
	current = head
	temp = head
	previous = None

	# check if list doesn't have any node
	# if not then return
	if (head == None):
		print("\nList is empty")
		return None

	# check if list have single node
	# if yes then delete it and return
	if (current.next == current):
		head = None
		return None

	# move first node to last
	# previous
	while (current.next != head):
		previous = current
		current = current.next

	previous.next = current.next
	head = previous.next

	return head
