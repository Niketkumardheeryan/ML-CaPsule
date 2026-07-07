class deque:
    def __init__(self):
        self.items=[]

    def isEmpty(self):
        return self.item==[]

    def addRear(self,item):
        self.items.append(item)

    def addFront(self,item):
        self.items.insert(0,item)

    def removeFront(self):
        return self.pop()

    def removeRear(self):
        return self.pop(0)

    def size(self):
        return len(self.items)

d=deque()

d.addFront(10)
d.addRear(20)
print(d.size())


