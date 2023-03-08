from io import BytesIO


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

    def handle_request(self, url, request):
        if request is None:
            request = {}
        request = request | self.get_request_from_middlewares()
        controller = self.routes.get(url, self.routes.get('/notfound', None))
        if controller is None:
            return '404 : Not Found', 'Page not found.'
        return '200 : OK', controller(request=request)

    def get_request_data(self, environ):
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(
            content_length).decode(encoding='utf-8') if content_length > 0 else b''
        return data

    def __call__(self, environ, start_response):
        request = None
        method = environ['REQUEST_METHOD']
        url = self.get_url(environ)
        if method == 'POST':
            request = {'data': self.get_request_data(environ)}
            url = f"/{url.split('/')[-1]}"

        code, content = self.handle_request(url, request=request)
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
