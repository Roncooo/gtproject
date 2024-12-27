class Stack:
    '''
    Apparently Pyhton does not have a built-in or library made stack with the top operation
    and we need it, so here our own implementation of a Stack.
    Note that this initializes as empty, and not with a single zero.
    '''
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("pop from empty stack")
    def top(self):
        if not self.is_empty():
            return self.stack[-1]  # Access the last element
        raise IndexError("top from empty stack")
    def safe_top_just_for_print(self):
        if self.is_empty():
            return []
        else:
            return self.top()
    def is_empty(self):
        return len(self.stack) == 0
    def size(self):
        return len(self.stack)
    def __str__(self):
        return str(self.stack) if self.stack else "[]"