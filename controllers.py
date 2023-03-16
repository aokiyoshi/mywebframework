from mywebframework.router import Router
from mywebframework.template_engine import render
from models import Course, Category, CourseType
from settings import DB_NAME
import json

router = Router()


def get_default_context(request):
    return dict(
        date=request.get('date', None),
        types=request.get('types', None),
    )


# Статичные страницы
@router.route('')
def main(request):
    return render('index.html', **get_default_context(request))


@router.route('/about')
def about(request):
    return render('about.html', **get_default_context(request))


# Курсы
@router.route('/courses')
def courses(request):
    if category_id := request.get('category'):
        data = Course(DB_NAME).select_many(category=category_id)
    else:
        data = Course(DB_NAME).select_all()

    if type_id := request.get('type'):
        data = Course(DB_NAME).select_many(type=type_id)
    else:
        data = Course(DB_NAME).select_all()

    for item in data:
        category_id = item['category']
        type_id = item['type']

        if category_id is None:
            item['category'] = 'Без категории'
            continue

        if type_id is None:
            item['type'] = 'Без типа'
            continue

        category = Category(DB_NAME).select(id=category_id)
        course_type = CourseType(DB_NAME).select(id=category_id)

        if not category:
            item['category'] = 'Без категории'
            continue

        if not course_type:
            item['type'] = 'Без типа'
            continue

        item['category'] = category['title']
        item['type'] = course_type['title']

    return render('courses_list.html', **get_default_context(request), data=data)


@router.route('/courses/create')
def create_course(request):
    categories = Category(DB_NAME).select_all()
    return render('create_course.html', **get_default_context(request), categories=categories)


@router.route('/courses/create/post')
def create_course_post(request):
    data = json.loads(request.get('data'))
    Course(DB_NAME).insert(**data)
    return '201 : Created'


@router.route('/courses/delete')
def delete_course(request):
    id = request.get('id')
    Course(DB_NAME).delete(id=id)
    return render('redirect.html', **get_default_context(request), url='/courses')


@router.route('/courses/dublicate')
def dublicate_course(request):
    id = request.get('id')
    course_data = Course(DB_NAME).select(id=id)
    course_data.pop('id')
    Course(DB_NAME).insert(**course_data)
    return render('redirect.html', **get_default_context(request), url='/courses')


@router.route('/courses/edit')
def edit_course(request):
    id = request.get('id')
    course_data = Course(DB_NAME).select(id=id)
    categories = Category(DB_NAME).select_all()
    return render('edit_course.html', **get_default_context(request), categories=categories, course_data=course_data)


@router.route('/courses/edit/post')
def edit_course_post(request):
    id = request.get('id')
    data = json.loads(request.get('data'))
    Course(DB_NAME).update(new_data=data, id=id)
    return '201 : Created'


# Категории
@router.route('/categories')
def categories(request):
    data = Category(DB_NAME).select_all()
    return render('categories.html', **get_default_context(request), data=data)


@router.route('/categories/create')
def create_category(request):
    categories = Category(DB_NAME).select_all()
    return render('create_category.html', **get_default_context(request), categories=categories)


@router.route('/categories/create/post')
def create_category_post(request):
    data = json.loads(request.get('data'))
    Category(DB_NAME).insert(**data)
    return render('redirect.html', **get_default_context(request), url='/categories')


@router.route('/categories/delete')
def delete_category(request):
    id = request.get('id')
    Category(DB_NAME).delete(id=id)
    return render('redirect.html', **get_default_context(request), url='/categories')


@router.route('/categories/edit')
def edit_category(request):
    id = request.get('id')
    category_data = Category(DB_NAME).select(id=id)
    return render('edit_category.html', **get_default_context(request), category_data=category_data)


@router.route('/categories/edit/post')
def edit_category_post(request):
    id = request.get('id')
    data = json.loads(request.get('data'))
    Category(DB_NAME).update(new_data=data, id=id)
    return '201 : Created'


@router.route('/categories/dublicate')
def dublicate_online(request):
    id = request.get('id')
    category_data = Category(DB_NAME).select(id=id)
    category_data.pop('id')
    Category(DB_NAME).insert(**category_data)
    return render('redirect.html', **get_default_context(request), url='/categories')


# 404
@router.route('/notfound')
def not_found(request):
    return render('404.html')


# Прочее

@router.route('/send')
def send_msg(request):
    print(f"Пользователь отправил нам сообщение: {request.get('data')}")
    return '201 : Created'


@router.route('/help')
def help(request):
    return render('help.html', **get_default_context(request))


@router.route('/contact')
def contact(request):
    return render('contact.html', **get_default_context(request))


@router.route('/login')
def contact(request):
    return render('login.html', **get_default_context(request))


@router.route('/auth')
def contact(request):
    return 'ok'
