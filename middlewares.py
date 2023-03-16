from datetime import date

from mywebframework.middleware import Middlewares
from models import CourseType
from settings import DB_NAME

middlewares = Middlewares()


@middlewares.register()
def main(request):
    request['date'] = date.today()
    


@middlewares.register()
def course_types(request):
    request['types'] = CourseType(DB_NAME).select_all()
