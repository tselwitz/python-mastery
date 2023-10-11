from functools import wraps


def logged(func):
    print('Adding logging to', func.__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper

# Define a new decorator @logformat(fmt) that accepts a format string as an
# argument and uses fmt.format(func=func) to format a supplied function
# into a log message:


def logformat(fmt):
    def logged(func):
        print('Adding logging to', func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(fmt.format(func=func))
            return func(*args, **kwargs)
        return wrapper
    return logged


if __name__ == "__main__":
    @logformat('{func.__code__.co_filename}:{func.__name__}')
    def add(x, y):
        print(x+y)
    add(2, 43)
