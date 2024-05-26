class Queue:
    def __init__(self):
        self.queue=[]

    def enqueue(self,item):
        self.queue.append(item)

    def dequeue(self):
        if(len(self.queue)<1):
            return None
        return self.queue.pop(0)

    def display(self):
        print(self.queue)

q=Queue()
q.enqueue(10)
q.enqueue(100)
q.dequeue()
q.display()


