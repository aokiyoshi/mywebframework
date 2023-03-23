

class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)


def debug(logger=None):
    def decorator(function):
        def wrapper(*args, **kwargs):
            arguments = f'{", ".join(args)}'
            k_arguments = f'{", ".join([f"{key}={value}" for key, value in kwargs.items()])}'
            if logger:
                logger.log(f"{function.__name__}({arguments}{k_arguments})")
            else:
                print(f"{function.__name__}({arguments}{k_arguments})")
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator