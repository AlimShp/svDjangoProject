from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def register(request):
    return render(request, 'registration.html', {'subtitle': ': Регистрация'})

@csrf_exempt
def login(request):
    return render(request, 'login.html', {'subtitle': ': Авторизация'})