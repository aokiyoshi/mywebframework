from io import BytesIO


class Framework:
    def __init__(self, routes, middlewares=None):
        self.routes = routes.get_routes()
        self.middlewares = middlewares.get_middlewares()

    def get_url(self, environ):
        """
        Gets url name from env and delete the backslash from the end if
        it exists
        """
        path = environ['PATH_INFO']
        if path.endswith('/'):
            path = path[:-1]
        return path

    def get_request_from_middlewares(self):
        """
        Gets data from middlewares
        """
        if self.middlewares is None:
            return {}
        request = {}
        for m in self.middlewares:
            m(request)
        return request

    def handle_request(self, url, request, is_post=False):
        """
        Gets request data if it exist, adds data from middleware
        """

        request = request | self.get_request_from_middlewares()
        controller = self.routes.get(url, self.routes.get('/notfound', None))

        if controller is None:
            return '404 : Not Found', 'Url not found.'

        if is_post:
            return '201 : Created', controller(request=request)

        return '200 : OK', controller(request=request)

    def get_request_data(self, environ):
        """
        Gets data from wsgi input and decode it.
        """
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0

        data = environ['wsgi.input'].read(
            content_length).decode(encoding='utf-8') if content_length > 0 else b''

        return data

    def __call__(self, environ, start_response):

        is_post = False
        request = {}
        method = environ['REQUEST_METHOD']
        url = self.get_url(environ)
        query_str = environ['QUERY_STRING']

        if method == 'POST':
            is_post = True
            request = {'data': self.get_request_data(environ)}

        if query_str:
            query_splitted = query_str.split('=')
            request[query_splitted[0]] = query_splitted[1]

        code, content = self.handle_request(url, request=request, is_post=is_post)

        start_response(code, [('Content-Type', 'text/html')])
        return [content.encode('utf-8')]
