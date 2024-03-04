from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

isAuth = False

@csrf_exempt
def index(request):
    global isAuth
    if isAuth and request.method == "GET":
        return render(request, 'profile.html')
    if request.method == "POST" and isAuth:
        isAuth = False
    return render(request, 'index.html')

@csrf_exempt
def register(request):

    return render(request, 'registration.html', {'subtitle': ': Регистрация'})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        global isAuth
        isAuth = True
        return redirect('/')
    return render(request, 'login.html', {'subtitle': ': Авторизация'})