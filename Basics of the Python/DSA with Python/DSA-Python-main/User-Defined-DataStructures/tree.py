
class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def inorder(root):
    if root:
        #left ,root ,right
        inorder(root.left)
        print(root.value)
        inorder(root.right)

def postorder(root):
    if root:
        #left,right,root
        postorder(root.left)
        postorder(root.right)
        print(root.value)


def preorder(root):
    if root:
        #root,left,right
        print(root.value)
        preorder(root.left)
        preorder(root.right)




def count_nodes(root):
    if root is None:
        return 0
    return (1 + count_nodes(root.left) + count_nodes(root.right))



def height(root):
    if root is None:
        return -1

    left_height = height(root.left)
    right_height = height(root.right)

    return ( 1 + max(left_height,right_height))

    



root=Node(1)
root.left=Node(2)
root.right=Node(3)
root.left.left=Node(4)



ok=count_nodes(root)
print(ok)














