from wsgiref.simple_server import make_server

from mywebframework.main import Framework
from controllers import router
from middlewares import middlewares

application = Framework(router, middlewares)

with make_server('', 8080, application) as httpd:
    print("Сервер запущен на порту 8080...")
    httpd.serve_forever()
