from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from carts.models import Cart
from orders.models import Order, OrderItem
from .models import User
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse


from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm, UserForgotPasswordForm, CustomPasswordChangeForm

import secrets
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Главная - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        if 'profile_submit' in request.POST:
            profile_form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
            print('0')
            if profile_form.is_valid():
                print('1')
                profile_form.save()
                print('2')
                messages.success(request, "Профиль успешно обновлен")
                return HttpResponseRedirect(reverse('users:profile'))
        elif 'password_submit' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request,
                                         password_form.user)  # Важно для предотвращения выхода пользователя из системы
                messages.success(request, "Пароль успешно обновлен")
                return HttpResponseRedirect(reverse('users:profile'))
    else:
        profile_form = ProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("sizeproduct"),
        )
    ).order_by("-id")

    context = {
        'title': 'Главная - Профиль',
        'form': profile_form,
        'password_form': password_form,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)


def users_cart(request):
    return render(request, 'users/users_cart.html')


fromaddr = 'demenkovakatarina@mail.ru'
mypass = "93XqCqhdZgaTje3KUut0"


def send(msg: MIMEMultipart, toaddr: str):
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def forgot_password(request):
    if request.method == 'POST':

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for i in range(12))

        form = UserForgotPasswordForm(data=request.POST)

        if form.is_valid():

            email = request.POST['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.warning(request, 'Пользователя с таким email не существует.')
                print(messages)
                # messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
                return HttpResponseRedirect(reverse('users:forgot_password'))

            user.set_password(password)
            user.save()

            username = user.username

            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = user.email
            msg['Subject'] = f"Восстановить доступ к аккаунту"

            body = f"<p>Ваш новый пароль: <strong>{password}</strong> для аккаунта с логином: <strong>{username}</strong></p><p>Используйте его для входа в аккаунт.</p>"
            msg.attach(MIMEText(body, 'html'))

            send(msg, user.email)

            return HttpResponseRedirect(reverse('users:login'))

    else:
        form = UserForgotPasswordForm()

    context = {
        'title': 'Home - Восстановить пароль',
        'form': form
    }

    return render(request, 'users/forgot_password.html')


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))
