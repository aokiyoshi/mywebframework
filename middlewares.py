from datetime import date

from mywebframework.main import Middlewares

middlewares = Middlewares()


@middlewares.register()
def main(request):
    request['date'] = date.today()
