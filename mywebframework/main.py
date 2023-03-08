class Framework:
    def __init__(self, routes, middlewares=None):
        self.routes = routes.get_routes()
        self.middlewares = middlewares.get_middlewares()

    def get_url(self, environ):
        path = environ['PATH_INFO']
        if path.endswith('/'):
            path = path[:-1]
        return path

    def get_request_from_middlewares(self):
        if self.middlewares is None:
            return {}
        request = {}
        for m in self.middlewares:
            m(request)
        return request

    def get_page(self, url):
        request = self.get_request_from_middlewares()
        controller = self.routes.get(url, self.routes.get('/notfound', None))
        if controller is None:
            return '404 : Not Found', 'Page not found.'
        return '200 : OK', controller(request=request)

    def __call__(self, environ, start_response):
        code, content = self.get_page(self.get_url(environ))
        start_response(code, [('Content-Type', 'text/html')])
        return [content.encode('utf-8')]


class Router:
    def __init__(self):
        self.routes = {}

    def route(self, path, **options):
        def decorator(f):
            self.routes[path] = f
            return f
        return decorator

    def get_routes(self):
        return self.routes


class Middlewares:
    def __init__(self):
        self.middlewares = []

    def register(self):
        def decorator(f):
            self.middlewares.append(f)
            return f
        return decorator

    def get_middlewares(self):
        return self.middlewares
