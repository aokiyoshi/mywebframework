from waitress import serve

from mywebframework.main import Framework
from controllers import router
from middlewares import middlewares

application = Framework(router, middlewares)

serve(application, listen='*:8080')