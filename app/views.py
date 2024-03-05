import random

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app.form import ImageForm
from app.models import ModelReg, ProfileImg


@csrf_exempt
def index(request):
    user_session = request.COOKIES.get('user_session')
    if user_session:
        print('Есть куки: ' + user_session)
        users = ModelReg.objects.all()
        for u in users:
            if u.user_session == user_session:
                print(request.method)
                print(u.user_image)
                profile_img = 'base_profile.jpg'
                if u.user_image:
                    profile_img = u.user_image
                print(profile_img)
                # if request.method == "GET":
                #     form = ImageForm()
                #     return render(request, 'profile.html', {'user': u.name, 'profile_image': profile_img, 'form': form})
                if request.method == "POST":
                    # проверка, что нажата кнопка Выйти
                    if 'logout' in request.POST:
                        print('Пользователь вышел')
                        html = render(request, 'index.html')
                        html.delete_cookie('user_session')
                        return html
                    if 'back' in request.POST:
                        profile_img = 'base_profile.jpg'
                    if 'load' in request.POST:
                        profile_img = '8.jpg'
                        form = ImageForm(request.POST, request.FILES)
                        if form.is_valid():
                            fname = request.FILES['user_image'].name
                            print(fname)
                            print(rename_image(fname, u.id))
                            form.save()

                            #added_image = ProfileImg.objects.last()
                        # return render(request, 'profile.html',
                        #               {'user': u.name, 'profile_image': profile_img, 'form': form})



                form = ImageForm()
                return render(request, 'profile.html', {'user': u.name, 'profile_image': profile_img, 'form': form})
        else:
            print('Куки удалены')
            html = render(request, 'index.html')
            html.delete_cookie('user_session')
            return html
    print('Нет куки')
    return render(request, 'index.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        users = ModelReg.objects.all()
        for u in users:
            if request.POST['email'] == u.email:
                return render(request, 'registration.html', {'subtitle': ': Регистрация', 'form': f'Пользователь с почтой {u.email} уже зарегистрирован!'})
        reg = ModelReg()
        reg.email = request.POST['email']
        reg.password = request.POST['pass']
        reg.name = request.POST['name']
        reg.user_session = generate_session(reg.email)
        reg.save()
        html = redirect('/')
        html.set_cookie('user_session', reg.user_session)
        return html
    return render(request, 'registration.html', {'subtitle': ': Регистрация'})


@csrf_exempt
def login(request):
    answer = ''
    if request.method == 'POST':
        users = ModelReg.objects.all()
        for u in users:
            if request.POST['email'] == u.email:
                if request.POST['pass'] == u.password:
                    # new session key for user
                    u.user_session = generate_session(u.email)
                    u.save(force_update=True)
                    html = redirect('/')
                    html.set_cookie('user_session', u.user_session)
                    return html
                else:
                    answer = 'Неправильный пароль!'
            else:
                answer = 'Неверное имя пользователя!'
    return render(request, 'login.html', {'subtitle': ': Авторизация', 'form': answer})

def generate_session(key: str):
    key = str(abs(key.__hash__()))
    key += '_'
    while len(key) < 48:
        key += chr(random.randint(65, 90))
    return key

def rename_image(fname: str, user_id: int):
    new_fname = 'IMG-' + str(user_id) + '.' + fname.split('.')[-1]
    return new_fname
