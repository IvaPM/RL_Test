import time
from cachedFunction import CachedFunction

def cache(function):

    cached_functions = {}

    def wrapper_function(*args, **kwargs):
        key = function.__name__+str(args)+str(kwargs)
        if key in cached_functions:
            cached_function=cached_functions.get(key)
            if cached_function.countdown_time>time.time() and cached_function.counter<11:
                cached_function.increase_counter()
                print("cached returned {} result {}".format(key, cached_function.cached))
                return cached_function.cached
            else:
                cached = function(*args, **kwargs)
                cached_functions[key] = CachedFunction(cached)
                print("function call returned {} result {}".format(key, cached))
                return cached
        else:
            cached = function(*args, **kwargs)
            cached_functions[key] = CachedFunction(cached)
            print("function call returned {} result {}".format(key, cached))
            return cached
        
    return wrapper_function

@cache
def add(a, b):
    return a+b

@cache
def multiply(a, b=1):
    return a*b


add(1,2)
add(1,2)
add(1,3)
multiply(1)
multiply(2, b=3)
multiply(1)
[add(1,3) for x in range(13)]
multiply(2, b=3)
time.sleep(300)
multiply(2, b=3)
multiply(2, b=3)


