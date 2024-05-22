class Node:
    def __init__(self,key):
        self.key=key
        self.left=None
        self.right=None



def insert(node,key):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left,key)
    else:
        node.right = insert(node.right,key)
    return node



def search(node,key):
    if node is None:
        return node

    if key == node.key:
        return  node

    if key > node.key:
        return search(node.right,key)

    if key < node.key:
        return search(node.left,key)


# to find in-order succesor
def minValueNode(node):
    current=node
    
    while(current.left is not None):
        current=current.left
    return current



def deleteNode(root, key):

 # Return if the tree is empty
    if root is None:
        return root

 # Find the node to be deleted
    if key < root.key:
        root.left = deleteNode(root.left, key)

    elif(key > root.key):
        root.right = deleteNode(root.right, key)

    else:
 # If the node is with only one child or no child
        if root.left is None:
            temp = root.right
            root = None
            return temp

        elif root.right is None:
            temp = root.left
            root = None
            return temp
 # If the node has two children,
 # place the inorder successor in position of the node to be deleted
        temp = minValueNode(root.right)
        root.key = temp.key
 # Delete the inorder successor
        root.right = deleteNode(root.right, temp.key)
    return root














root = None
root = insert(root,12)
root = insert(root,23)
root = insert(root,10)
root = insert(root,100)

ok=search(root,100)
print(ok)

root=deleteNode(root,100)

ok=search(root,100)
print(ok)








