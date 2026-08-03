def create_stack():
    stack=[]
    return stack

def check_empty(stack):
    return len(stack)==0

def push(stack,item):
    stack.append(item)
    print("pushed"+item)

def pop(stack):
    if(check_empty(stack)):
        return "stack is empty"
    else:
        return stack.pop()

stack=create_stack()
push(stack,str(6))
push(stack,str(9))
pop(stack)
print(stack)



