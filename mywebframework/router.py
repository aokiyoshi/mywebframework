class Router:
    """
    Provides route decorators for controllers
    """
    def __init__(self):
        self.routes = {}

    def route(self, path, **options):
        def decorator(f):
            self.routes[path] = f
            return f
        return decorator

    def get_routes(self):
        return self.routes