class Middlewares:
    """
    Provides decorator for register middleware functions
    """

    def __init__(self):
        self.middlewares = []

    def register(self):
        def decorator(f):
            self.middlewares.append(f)
            return f
        return decorator

    def get_middlewares(self):
        return self.middlewares
