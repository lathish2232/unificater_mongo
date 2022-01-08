"""
This is the example how to use this package
@clearable_lru_cache()
def foo(x):
    print('foo', x)

@clearable_lru_cache()
def bar(x):
    print('bar', x)

for i in [1, 2]:
    for j in [1, 2]:
        print('Calling functions')
        for k in [1, 2, 3]:
            for f in [foo, bar]:
                f(k)
        print('Functions called - if you saw nothing they were cached')
    print('Clearing cache')
    clear_all_cached_functions()
"""

from functools import lru_cache
cached_functions = []

def clearable_lru_cache(*args, **kwargs):
    def decorator(func):
        func = lru_cache(*args, **kwargs)(func)
        cached_functions.append(func)
        return func

    return decorator

def clear_all_cached_functions():
    for func in cached_functions:
        func.cache_clear()

