import os
import random

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app.form import ImageForm
from app.models import ModelReg


hasBotStarted = False
bot_button = ["Запустить", "Остановить"]
image_dir = 'app/static/img/'


@csrf_exempt
def index(request):
    global hasBotStarted
    user_session = request.COOKIES.get('user_session')
    if user_session:
        print('Есть куки: ' + user_session)
        users = ModelReg.objects.all()
        for u in users:
            if u.user_session == user_session:
                profile_img = 'base_profile.jpg'
                if u.user_image:
                    profile_img = u.user_image
                if request.method == "POST":
                    # проверка, что нажата кнопка Выйти, и удаление пользовательской сессии
                    if 'logout' in request.POST:
                        print('Пользователь вышел')
                        html = render(request, 'index.html')
                        html.delete_cookie('user_session')
                        return html
                    if 'tbot' in request.POST:
                        # проверка состояния бота на соответствие отображаемой кнопки у юзера
                        if bot_button[hasBotStarted] == u.bot_btn:
                        #if True:
                            if hasBotStarted:
                                profile_img = u.user_image
                                hasBotStarted = False
                            else:
                                profile_img = 'base_profile.jpg'
                                hasBotStarted = True
                        else:
                            answer = "Cостояние бота уже было изменено другим пользователем"
                            print(answer)
                        u.bot_btn = bot_button[hasBotStarted]
                        print(hasBotStarted)
                        print(u.bot_btn)
                        u.save(force_update=True)

                    # загрузка изображения
                    if 'load' in request.POST:
                        form = ImageForm(request.POST, request.FILES)
                        if form.is_valid():
                            fname = request.FILES['user_image'].name
                            if u.user_image:
                                # удаляем старое изображение
                                os.remove(image_dir + u.user_image)
                            form.save()
                            # добавляем новое
                            new_fname = rename_image(fname, u.id)
                            os.rename(image_dir + fname, image_dir + new_fname)
                            u.user_image = new_fname
                            u.save(force_update=True)
                            profile_img = u.user_image

                form = ImageForm()
                return render(request, 'profile.html', {'user': u, 'profile_image': profile_img, 'form': form})
        else:
            # удаляем куки с сессией, если пользователь с таким сессионным ключом не найден
            html = render(request, 'index.html')
            html.delete_cookie('user_session')
            return html
    print('Нет куки')
    return render(request, 'index.html')


@csrf_exempt
def register(request):
    global hasBotStarted
    global bot_button
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
        reg.bot_btn = bot_button[hasBotStarted]
        print(hasBotStarted)
        print(u.bot_btn)
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
                    u.bot_btn = bot_button[hasBotStarted]
                    print(hasBotStarted)
                    print(u.bot_btn)
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
    new_fname = 'IMG-' + str(user_id) + '-'
    for i in range(5):
        new_fname += chr(random.randint(65, 90))
    new_fname += '.' + fname.split('.')[-1]
    return new_fname
