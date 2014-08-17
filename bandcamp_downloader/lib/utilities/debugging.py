from functools import wraps

def debug(func):
    # func is function to be wrapped
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("+++", func.__qualname__)
        return func(*args, **kwargs)
    return wrapper

def debugmethods(cls):
    for key, value in vars(cls).items():
        if callable(value):
            setattr(cls, key, debug(value))
    return cls
    
if __name__ == "__main__":
    @debug
    def add(a, b):
        print(a + b)
        
    @debug
    def sub(a, b):
        print(a - b)
        
    @debugmethods
    class Test:
        def method1(self):
            print("in method1")
            
        def method2(self):
            print("in method2")

    add(1, 2)
    add(3, 4)
    
    sub(1, 2)
    sub(3, 4)
    
    t = Test()
    t.method1()
    t.method2()