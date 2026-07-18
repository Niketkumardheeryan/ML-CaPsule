
class Node:

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
       
 



def insert(node, value):

    if not node:
        return Node(value)

 # insert value
    if value == node.value:
        pass
    elif value < node.value:
        node.left = insert(node.left, value)
    else:
        node.right = insert(node.right, value)
        
    return node