from functools import wraps

def data(values):
    def wrapper(func):
        setattr(func, 'values', values)
        return func
    return wrapper


def ddt(cls):
    def run_with(func, *args, **kwargs):
        @wraps(func)
        def wrapper(self):
            return func(self, *args, **kwargs)
        return wrapper

    for name, f in cls.__dict__.items():
        if hasattr(f, 'values'):
            i = 0
            for v in f.values:
                setattr(cls, 
                        "{0}_{1}".format(name, v), 
                        run_with(f, v))
                i = i + 1
            delattr(cls, name)
            #print(dir(cls))
    return cls

