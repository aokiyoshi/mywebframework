class FakeApp:
    def __call__(self, environ, start_response):
        start_response('200 : OK', [('Content-Type', 'text/html')])
        return ['Hello from Fake'.encode('utf-8')] 