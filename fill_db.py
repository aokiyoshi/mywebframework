from models import User, Course, Category, CourseType
from settings import DB_NAME

categories = [
    {
        'title': 'Курсы python',
        'desc': 'В курсе преподаватель будет рассказывать все про python'
    },
    {
        'title': 'Курсы по rust',
        'desc': 'Курс по основам rust для новичков. Покрывает базовые темы и немного стандартной библиотеки'
    },
]

for course in categories:
    Category(DB_NAME).insert(**course)


types = [
    {
        'title': 'Оффлайн занятия',
        'desc': 'Предполагается, что занатия будет проходит вживую, в аудитории.'
    },
    {
        'title': 'Онлайн вебинары',
        'desc': 'Онлайн вебинары, в реальном времени'
    },
    {
        'title': 'Записи уроков',
        'desc': 'Записи уроков'
    },
]

for course_type in types:
    CourseType(DB_NAME).insert(**course_type)


categories = [
    {
        'title': 'Курсы python',
        'desc': 'В курсе преподаватель будет рассказывать все про python'
    },
    {
        'title': 'Курсы по rust',
        'desc': 'Курс по основам rust для новичков. Покрывает базовые темы и немного стандартной библиотеки'
    },
]

for course in categories:
    Category(DB_NAME).insert(**course)

courses = [
    {
        'title': 'Курс по python',
        'category': 1,
        'type': 1,
        'desc': 'Курс по основам python для новичков. Покрывает базовые темы и немного стандартной библиотеки'
    },
    {
        'title': 'Курс по rust',
        'category': 2,
        'type': 2,
        'desc': 'Курс по основам rust для новичков. Покрывает базовые темы и немного стандартной библиотеки'
    },
]

for course in courses:
    Course(DB_NAME).insert(**course)


users = [
    {
        'username': 'john97',
        'first_name': 'John',
        'last_name': 'Smith',
        'password': 'Sds55wee!',
    },
    {
        'username': 'super48',
        'first_name': 'Bryan',
        'last_name': 'Johnson',
        'password': '1231sWcc@',
    },
]

for user in users:
    User(DB_NAME).create_user(**user)