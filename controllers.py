from mywebframework.main import Router
from mywebframework.template_engine import render

router = Router()


@router.route('')
def main(request):
    return render('index.html', date=request.get('date', None))


@router.route('/about')
def about(request):
    return render('about.html')


@router.route('/help')
def help(request):
    return render('help.html')


@router.route('/contact')
def contact(request):
    return render('contact.html')


@router.route('/notfound')
def not_found(request):
    return render('404.html')


@router.route('/send')
def send_msg(request):
    print(f"Пользователь отправил нам сообщение: {request.get('data')}")
    return 'hello'
