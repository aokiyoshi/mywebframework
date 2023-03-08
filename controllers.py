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
    return 'help page!'


@router.route('/notfound')
def not_found(request):
    return render('404.html')
