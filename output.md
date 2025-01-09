## **Файл: /Users/katedem/PycharmProjects/shop-passag/output.docx**
Не удалось прочитать содержимое файла: 'utf-8' codec can't decode byte 0xad in position 14: invalid start byte
## **Файл: /Users/katedem/PycharmProjects/shop-passag/.DS\_Store**
Не удалось прочитать содержимое файла: 'utf-8' codec can't decode byte 0x80 in position 3131: invalid start byte
## **Файл: /Users/katedem/PycharmProjects/shop-passag/requirements.txt**
appnope==0.1.4
asgiref==3.7.2
asttokens==2.4.1
colorama==0.4.6
decorator==5.1.1
Django==4.2.7
djangorestframework==3.15.1
et-xmlfile==1.1.0
exceptiongroup==1.2.1
executing==2.0.1
ipython==8.17.2
jedi==0.19.1
matplotlib-inline==0.1.6
openpyxl==3.1.3
parso==0.8.3
pexpect==4.9.0
Pillow==10.1.0
prompt-toolkit==3.0.41
psycopg2==2.9.9
ptyprocess==0.7.0
pure-eval==0.2.2
Pygments==2.17.1
six==1.16.0
sqlparse==0.4.4
stack-data==0.6.3
traitlets==5.13.0
typing\_extensions==4.8.0
tzdata==2023.3
wcwidth==0.2.10
## **Файл: /Users/katedem/PycharmProjects/shop-passag/README.MD**
THIS ONLINE SHOP WEBSITE.
## **Файл: /Users/katedem/PycharmProjects/shop-passag/.gitignore**
#python stuff
venv/
.pylintrc
\_\_pycache\_\_/

#ide stuff
.vscode
.idea

#django stuff
db.sqlite3
media/
## **Файл: /Users/katedem/PycharmProjects/shop-passag/manage.py**
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
`    `"""Run administrative tasks."""
`    `os.environ.setdefault('DJANGO\_SETTINGS\_MODULE', 'app.settings')
`    `try:
`        `from django.core.management import execute\_from\_command\_line
`    `except ImportError as exc:
`        `raise ImportError(
`            `"Couldn't import Django. Are you sure it's installed and "
`            `"available on your PYTHONPATH environment variable? Did you "
`            `"forget to activate a virtual environment?"
`        `) from exc
`    `execute\_from\_command\_line(sys.argv)


if \_\_name\_\_ == '\_\_main\_\_':
`    `main()
## **Файл: /Users/katedem/PycharmProjects/shop-passag/script.py**
import os
from docx import Document

def create\_doc\_from\_folder(folder\_path, output\_file, exclude\_dirs=None):
`    `if exclude\_dirs is None:
`        `exclude\_dirs = []

`    `# Создаём новый документ Word
`    `doc = Document()

`    `print(f"Начинаем обработку папки: {folder\_path}")
`    `print(f"Исключаем папки (включая вложенные): {exclude\_dirs}")

`    `# Проходим по всем файлам и папкам внутри указанной директории
`    `for root, dirs, files in os.walk(folder\_path):
`        `# Исключаем папки из обработки, включая вложенные
`        `dirs[:] = [d for d in dirs if d not in exclude\_dirs]
`        `print(f"Обрабатываем директорию: {root}")
`        `print(f"Найдены файлы: {files}")

`        `for file in files:
`            `file\_path = os.path.join(root, file)  # Полный путь к файлу
`            `try:
`                `print(f"Читаем файл: {file\_path}")
`                `# Попытка открыть файл и прочитать содержимое
`                `with open(file\_path, 'r', encoding='utf-8') as f:
`                    `content = f.read()

`                `# Добавляем в документ заголовок с именем файла и его путём
`                `doc.add\_heading(f"Файл: {file\_path}", level=2)
`                `doc.add\_paragraph(content)
`                `print(f"Файл успешно добавлен: {file\_path}")

`            `except (UnicodeDecodeError, IOError) as e:
`                `# Если файл не удаётся прочитать (например, бинарный)
`                `print(f"Ошибка при чтении файла {file\_path}: {e}")
`                `doc.add\_heading(f"Файл: {file\_path}", level=2)
`                `doc.add\_paragraph(f"Не удалось прочитать содержимое файла: {e}")

`    `# Сохраняем документ
`    `doc.save(output\_file)
`    `print(f"Документ успешно создан: {output\_file}")

\# Путь к папке, содержимое которой нужно обработать
folder\_path = input("Введите путь к папке: ").strip()
\# Список папок для исключения (включая вложенные)
exclude\_dirs = ["media", "venv", "static", "\_\_pycache\_\_", "migrations", "app", ".git", ".idea"]  # Укажите названия папок, которые нужно исключить
\# Имя выходного файла
output\_file = "output.docx"

create\_doc\_from\_folder(folder\_path, output\_file, exclude\_dirs)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/models.py**
from django.db import models
from goods.models import Products, SizeProductRelation

from users.models import User


class CartQueryset(models.QuerySet):

`    `def total\_price(self):
`        `return sum(cart.products\_price() for cart in self)

`    `def total\_quantity(self):
`        `if self:
`            `return sum(cart.quantity for cart in self)
`        `return 0


class Cart(models.Model):
`    `user = models.ForeignKey(to=User, on\_delete=models.CASCADE, blank=True, null=True, verbose\_name='Пользователь')
`    `sizeproduct = models.ForeignKey(to=SizeProductRelation, on\_delete=models.CASCADE, verbose\_name='Товар')
`    `quantity = models.PositiveSmallIntegerField(default=0, verbose\_name='Количество')
`    `session\_key = models.CharField(max\_length=32, null=True, blank=True)
`    `created\_timestamp = models.DateTimeField(auto\_now\_add=True, verbose\_name='Дата добавления')

`    `class Meta:
`        `db\_table = 'cart'
`        `verbose\_name = "Корзина"
`        `verbose\_name\_plural = "Корзина"
`        `ordering = ("id",)

`    `objects = CartQueryset().as\_manager()

`    `def products\_price(self):
`        `return round(self.sizeproduct.product.sell\_price() \* self.quantity, 2)

`    `def \_\_str\_\_(self):
`        `if self.user:
`            `return f'Корзина {self.user.username} | Товар {self.sizeproduct.product.name} | Количество {self.quantity}'

`        `return f'Анонимная корзина | Товар {self.sizeproduct.product.name} | Количество {self.quantity}'
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/\_\_init\_\_.py**

## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/apps.py**
from django.apps import AppConfig


class CartsConfig(AppConfig):
`    `default\_auto\_field = 'django.db.models.BigAutoField'
`    `name = 'carts'
`    `verbose\_name = 'Корзины'
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/admin.py**
from django.contrib import admin

from carts.models import Cart



class CartTabAdmin(admin.TabularInline):
`    `model = Cart
`    `fields = "sizeproduct", "quantity", "created\_timestamp"
`    `search\_fields = "sizeproduct", "quantity", "created\_timestamp"
`    `readonly\_fields = ("created\_timestamp",)
`    `extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
`    `list\_display = ["user\_display", "sizeproduct\_display", "quantity", "created\_timestamp",]
`    `list\_filter = ["created\_timestamp", "user", "sizeproduct\_\_product\_\_name",]

`    `def user\_display(self, obj):
`        `if obj.user:
`            `return str(obj.user)
`        `return "Анонимный пользователь"

`    `def sizeproduct\_display(self, obj):
`        `return str(obj.sizeproduct.product.name)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/utils.py**
from carts.models import Cart


def get\_user\_carts(request):
`    `if request.user.is\_authenticated:
`        `return Cart.objects.filter(user=request.user).select\_related('sizeproduct')

`    `if not request.session.session\_key:
`        `request.session.create()
`    `return Cart.objects.filter(session\_key=request.session.session\_key)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/tests.py**
from django.test import TestCase

\# Create your tests here.
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/urls.py**
from django.urls import path

from carts import views

app\_name = 'carts'

urlpatterns = [
`    `path('cart\_add/', views.cart\_add, name='cart\_add'),
`    `path('cart\_change/', views.cart\_change, name='cart\_change'),
`    `path('cart\_remove/', views.cart\_remove, name='cart\_remove'),
]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/views.py**
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render\_to\_string
from carts.models import Cart
from carts.utils import get\_user\_carts
from django.forms import ValidationError
from django.contrib import messages

from goods.models import Products, SizeProductRelation


def cart\_add(request):
`    `sizeproduct\_id = request.POST.get("product\_id")
`    `print(sizeproduct\_id)

`    `sizeproduct = SizeProductRelation.objects.get(id=sizeproduct\_id)
`    `# product = Products.objects.get(id=sizeproduct\_id)
`    `print(sizeproduct)

`    `if request.user.is\_authenticated:
`        `carts = Cart.objects.filter(user=request.user, sizeproduct=sizeproduct)

`        `if carts.exists():

`            `cart = carts.first()
`            `if cart:
`                `if sizeproduct.count == cart.quantity:
`                    `print('ошибка')
`                    `messages.error(request, 'Недостаточное количество товара на складе\
`                                           `В наличии - {sizeproduct.count}')
`                    `raise ValidationError(f'Недостаточное количество товара на складе\
`                                           `В наличии - {sizeproduct.count}')
`                `else:
`                    `cart.quantity += 1
`                    `cart.save()
`        `else:
`            `Cart.objects.create(user=request.user, sizeproduct=sizeproduct, quantity=1)

`    `else:
`        `carts = Cart.objects.filter(
`            `session\_key=request.session.session\_key, sizeproduct=sizeproduct)

`        `if carts.exists():
`            `cart = carts.first()
`            `if cart:
`                `if sizeproduct.count == cart.quantity:
`                    `response\_data = {
`                        `"message": f'Недостаточное количество товара на складе\
`                                           `В наличии - {sizeproduct.count}',
`                    `}

`                    `return JsonResponse(response\_data)
`                `else:
`                    `cart.quantity += 1
`                    `cart.save()
`        `else:
`            `Cart.objects.create(
`                `session\_key=request.session.session\_key, sizeproduct=sizeproduct, quantity=1)

`    `user\_cart = get\_user\_carts(request)
`    `cart\_items\_html = render\_to\_string(
`        `"carts/includes/included\_cart.html", {"carts": user\_cart}, request=request)

`    `response\_data = {
`        `"message": "Товар добавлен в корзину",
`        `"cart\_items\_html": cart\_items\_html,
`    `}

`    `return JsonResponse(response\_data)


def cart\_change(request):
`    `cart\_id = request.POST.get("cart\_id")
`    `quantity = request.POST.get("quantity")
`    `print(quantity)

`    `cart = Cart.objects.get(id=cart\_id)

`    `if int(quantity) > cart.sizeproduct.count:
`        `raise ValidationError(f'Недостаточное количество товара на складе\
`                                                   `В наличии - {cart.sizeproduct.count}')
`    `else:

`        `cart.quantity = quantity
`        `cart.save()
`        `updated\_quantity = cart.quantity

`    `cart = get\_user\_carts(request)
`    `cart\_items\_html = render\_to\_string(
`        `"carts/includes/included\_cart.html", {"carts": cart}, request=request)

`    `response\_data = {
`        `"message": "Количество изменено",
`        `"cart\_items\_html": cart\_items\_html,
`        `"quaantity": updated\_quantity,
`    `}

`    `return JsonResponse(response\_data)


def cart\_remove(request):
`    `cart\_id = request.POST.get("cart\_id")

`    `cart = Cart.objects.get(id=cart\_id)
`    `quantity = cart.quantity
`    `print(quantity)
`    `cart.delete()

`    `user\_cart = get\_user\_carts(request)
`    `cart\_items\_html = render\_to\_string(
`        `"carts/includes/included\_cart.html", {"carts": user\_cart}, request=request)

`    `response\_data = {
`        `"message": "Товар удален",
`        `"cart\_items\_html": cart\_items\_html,
`        `"quantity\_deleted": quantity,
`    `}

`    `return JsonResponse(response\_data)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/templatetags/carts\_tags.py**
from django import template

from carts.models import Cart
from carts.utils import get\_user\_carts

register = template.Library()


@register.simple\_tag()
def user\_carts(request):
`    `return get\_user\_carts(request)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/templatetags/\_\_init\_\_.py**

## **Файл: /Users/katedem/PycharmProjects/shop-passag/carts/templates/carts/includes/included\_cart.html**
{% load static %}

<div class="mb-3">
`    `{% for cart in carts %}
`        `<ul class="list-group">
`            `<li class="list-group-item" style="border-color: #ffffff">
`                `<div class="row">
`                    `<div class="col-2">
`                        `<img src="{{ cart.sizeproduct.product.image.url }}" alt="..." height="90px" width="65px">
`                    `</div>
`                    `<div class="col-6" style="padding-left: 30px">
`                        `<h5 class="card-title mb-1">{{ cart.sizeproduct.product.name }}</h5>
`                        `<p style="margin-top:0; margin-bottom: 0; font-size: 15px">{{ cart.sizeproduct.size.name }}</p>
`                        `<p style="margin-top:0; margin-bottom: 0">{% for color in cart.sizeproduct.product.color.all %} {{ color.name }} {% endfor %}</p>
`                        `<p class="mt-0">{% for consist in cart.sizeproduct.product.consist.all %} {{ consist.name }} {% endfor %}</p>
`                    `</div>
`                    `<div class="col-4">
`                        `<h5>{{cart.products\_price}} Р</h5>
`                        `<div class="btn-group btn-group-sm mt-2 input-group" role="group" aria-label="First group" style="max-width: 80px">
`                            `<button type="button" class="btn btn-outline-secondary decrement" data-cart-id="{{ cart.id }}" data-cart-change-url="{% url 'cart:cart\_change' %}" style="width: 20px">
`                                `{% csrf\_token %}
`                                `-</button>
`                            `<input type="text" class="form-control number" value="{{ cart.quantity }}" style="border-color: #4d5154; border-radius: 0; max-width: 25px; padding: 1px 8px 1px 5px;" readonly>
`                            `{% if cart.quantity < cart.sizeproduct.count %}
`                            `<button type="button" class="btn btn-outline-secondary increment" data-cart-id="{{ cart.id }}" data-cart-change-url="{% url 'cart:cart\_change' %}" style="width: 20px">
`                                `{% csrf\_token %}
`                                `+</button>
`                            `{% else %}
`                            `<button type="button" class="btn btn-outline-secondary" style="width: 20px" disabled>
`                                `+</button>
`                            `{% endif %}
`                        `</div>
`                        `<a href="{% url "cart:cart\_remove" %}" class="remove-from-cart"
`                           `data-cart-id="{{ cart.id }}" style="margin-top: 30px; margin-left: 5px" data-toggle="tooltip" data-placement="bottom" title="Удалить">
`                            `{% csrf\_token %}
`                            `<img class="mx-1" src="{% static "deps/icons/trash-red.svg" %}"
`                                `alt="Catalog Icon" width="20" height="20">
`                        `</a>
`                    `</div>
`                `</div>
`            `</li>
`            `<hr class="mt-0 mb-1">
`        `</ul>
`    `{% endfor %}
</div>
<div class="row">
`    `<h4 class="col-7 float-left"><strong>Итого</strong></h4>
`    `<h4 class="col-5"><strong>{{ carts.total\_price }} Р</strong></h4>
</div>
{% if carts and not order %}
`    `<div class="row">
`        `<div class="col-7"></div>
`        `<div class="col-5">
`            `<a class="btn mb-3 mt-2" style="background-color: #1d4d51; color: #e1d89f;" href="{% url 'orders:create\_order' %}">
`                `Оформить заказ
`            `</a>
`        `</div>
`    `</div>
{% endif %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/models.py**
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
`    `phone\_number = models.CharField(max\_length=10, blank=True, null=True)

`    `class Meta:
`        `db\_table = 'user'
`        `verbose\_name = 'Пользователя'
`        `verbose\_name\_plural = 'Пользователи'

`    `def \_\_str\_\_(self):
`        `return self.username
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/\_\_init\_\_.py**

## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/apps.py**
from django.apps import AppConfig


class UsersConfig(AppConfig):
`    `default\_auto\_field = 'django.db.models.BigAutoField'
`    `name = 'users'
`    `verbose\_name = 'Пользователи'
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/forms.py**
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm, PasswordChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):
`    `class Meta:
`        `model = User
`        `fields = ['username', 'password']

`    `username = forms.CharField()
`    `password = forms.CharField()


class UserForgotPasswordForm(PasswordResetForm):
`    `class Meta:
`        `model = User
`        `fields = ['email']

`    `email = forms.CharField()


class UserRegistrationForm(UserCreationForm):
`    `class Meta:
`        `model = User
`        `fields = (
`            `"first\_name",
`            `"last\_name",
`            `"username",
`            `"email",
`            `"phone\_number",
`            `"password1",
`            `"password2",
`        `)

`    `first\_name = forms.CharField()
`    `last\_name = forms.CharField()
`    `username = forms.CharField()
`    `email = forms.CharField()
`    `phone\_number = forms.CharField()
`    `password1 = forms.CharField()
`    `password2 = forms.CharField()


class ProfileForm(UserChangeForm):
`    `class Meta:
`        `model = User
`        `fields = (
`            `"first\_name",
`            `"last\_name",
`            `"phone\_number",
`            `"email",
`            `)

`    `first\_name = forms.CharField()
`    `last\_name = forms.CharField()
`    `email = forms.EmailField()
`    `phone\_number = forms.CharField()


class CustomPasswordChangeForm(PasswordChangeForm):
`    `old\_password = forms.CharField(label='Старый пароль',
`                                   `widget=forms.PasswordInput(attrs={'class': 'form-control'}))
`    `new\_password1 = forms.CharField(label='Новый пароль',
`                                    `widget=forms.PasswordInput(attrs={'class': 'form-control'}))
`    `new\_password2 = forms.CharField(label='Подтверждение нового пароля',
`                                    `widget=forms.PasswordInput(attrs={'class': 'form-control'}))
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/admin.py**
from django.contrib import admin
from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
`    `list\_display = ["username", "first\_name", "last\_name", "email", "phone\_number"]
`    `search\_fields = ["username", "first\_name", "last\_name", "email", "phone\_number"]

`    `inlines = [CartTabAdmin,OrderTabulareAdmin]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/tests.py**
from django.test import TestCase

\# Create your tests here.
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/urls.py**
from django.urls import path
from users import views

app\_name = 'users'
urlpatterns = [
`    `path('login/', views.login, name='login'),
`    `path('registration/', views.registration, name='registration'),
`    `path('profile/', views.profile, name='profile'),
`    `path('users-cart/', views.users\_cart, name='users\_cart'),
`    `path('logout/', views.logout, name='logout'),
`    `path('forgot\_password/', views.forgot\_password, name='forgot\_password'),
`    `path('orders', views.profile, name='orders'),

]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/views.py**
from django.contrib.auth.decorators import login\_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from carts.models import Cart
from orders.models import Order, OrderItem
from .models import User
from django.contrib.auth import update\_session\_auth\_hash
from django.http import JsonResponse


from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm, UserForgotPasswordForm, CustomPasswordChangeForm

import secrets
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def login(request):
`    `if request.method == 'POST':
`        `form = UserLoginForm(data=request.POST)
`        `if form.is\_valid():
`            `username = request.POST['username']
`            `password = request.POST['password']
`            `user = auth.authenticate(username=username, password=password)

`            `session\_key = request.session.session\_key

`            `if user:
`                `auth.login(request, user)
`                `messages.success(request, f"{username}, Вы вошли в аккаунт")

`                `if session\_key:
`                    `Cart.objects.filter(session\_key=session\_key).update(user=user)

`                `redirect\_page = request.POST.get('next', None)
`                `if redirect\_page and redirect\_page != reverse('user:logout'):
`                    `return HttpResponseRedirect(request.POST.get('next'))

`                `return HttpResponseRedirect(reverse('main:index'))
`    `else:
`        `form = UserLoginForm()

`    `context = {
`        `'title': 'Home - Авторизация',
`        `'form': form
`    `}
`    `return render(request, 'users/login.html', context)


def registration(request):
`    `if request.method == 'POST':
`        `form = UserRegistrationForm(data=request.POST)
`        `if form.is\_valid():
`            `form.save()

`            `session\_key = request.session.session\_key

`            `user = form.instance
`            `auth.login(request, user)

`            `if session\_key:
`                `Cart.objects.filter(session\_key=session\_key).update(user=user)
`            `messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
`            `return HttpResponseRedirect(reverse('main:index'))
`    `else:
`        `form = UserRegistrationForm()

`    `context = {
`        `'title': 'Главная - Регистрация',
`        `'form': form
`    `}
`    `return render(request, 'users/registration.html', context)


@login\_required
def profile(request):
`    `if request.method == 'POST':
`        `profile\_form = ProfileForm(instance=request.user)
`        `password\_form = CustomPasswordChangeForm(user=request.user)
`        `if 'profile\_submit' in request.POST:
`            `profile\_form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
`            `print('0')
`            `if profile\_form.is\_valid():
`                `print('1')
`                `profile\_form.save()
`                `print('2')
`                `messages.success(request, "Профиль успешно обновлен")
`                `return HttpResponseRedirect(reverse('users:profile'))
`        `elif 'password\_submit' in request.POST:
`            `password\_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
`            `if password\_form.is\_valid():
`                `password\_form.save()
`                `update\_session\_auth\_hash(request,
`                                         `password\_form.user)  # Важно для предотвращения выхода пользователя из системы
`                `messages.success(request, "Пароль успешно обновлен")
`                `return HttpResponseRedirect(reverse('users:profile'))
`    `else:
`        `profile\_form = ProfileForm(instance=request.user)
`        `password\_form = CustomPasswordChangeForm(user=request.user)

`    `orders = Order.objects.filter(user=request.user).prefetch\_related(
`        `Prefetch(
`            `"orderitem\_set",
`            `queryset=OrderItem.objects.select\_related("sizeproduct"),
`        `)
`    `).order\_by("-id")

`    `context = {
`        `'title': 'Главная - Профиль',
`        `'form': profile\_form,
`        `'password\_form': password\_form,
`        `'orders': orders,
`    `}
`    `return render(request, 'users/profile.html', context)


def users\_cart(request):
`    `return render(request, 'users/users\_cart.html')


fromaddr = 'demenkovakatarina@mail.ru'
mypass = "93XqCqhdZgaTje3KUut0"


def send(msg: MIMEMultipart, toaddr: str):
`    `server = smtplib.SMTP\_SSL('smtp.mail.ru', 465)
`    `server.login(fromaddr, mypass)
`    `text = msg.as\_string()
`    `server.sendmail(fromaddr, toaddr, text)
`    `server.quit()


def forgot\_password(request):
`    `if request.method == 'POST':

`        `characters = string.ascii\_letters + string.digits + string.punctuation
`        `password = ''.join(secrets.choice(characters) for i in range(12))

`        `form = UserForgotPasswordForm(data=request.POST)

`        `if form.is\_valid():

`            `email = request.POST['email']

`            `try:
`                `user = User.objects.get(email=email)
`            `except User.DoesNotExist:
`                `messages.warning(request, 'Пользователя с таким email не существует.')
`                `print(messages)
`                `# messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
`                `return HttpResponseRedirect(reverse('users:forgot\_password'))

`            `user.set\_password(password)
`            `user.save()

`            `username = user.username

`            `msg = MIMEMultipart()
`            `msg['From'] = fromaddr
`            `msg['To'] = user.email
`            `msg['Subject'] = f"Восстановить доступ к аккаунту"

`            `body = f"<p>Ваш новый пароль: <strong>{password}</strong> для аккаунта с логином: <strong>{username}</strong></p><p>Используйте его для входа в аккаунт.</p>"
`            `msg.attach(MIMEText(body, 'html'))

`            `send(msg, user.email)

`            `return HttpResponseRedirect(reverse('users:login'))

`    `else:
`        `form = UserForgotPasswordForm()

`    `context = {
`        `'title': 'Home - Восстановить пароль',
`        `'form': form
`    `}

`    `return render(request, 'users/forgot\_password.html')


@login\_required
def logout(request):
`    `messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
`    `auth.logout(request)
`    `return redirect(reverse('main:index'))
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/templates/users/profile.html**
{% extends "base.html" %}
{% load static %}
{% load carts\_tags %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block css %}
<style>
.nav {
`        `justify-content: center;
`        `border-bottom: none;
`        `margin-top: -10px;
`    `}
.nav-item {
`        `margin-left: 20px;
`    `}
.nav-link {
`        `font-size: 1.25rem;
`        `border: none;
`        `color: #6c757d;
`        `background-color: transparent;
`        `width: auto;
`        `padding-bottom: 5px;
`        `cursor: pointer;
`    `}
.nav-link:hover {
`        `color: #1d4d51;
`        `border-bottom: 2px solid #1d4d51;
`    `}
.nav-link.active {
`        `border-bottom: 2px solid #1d4d51;
`        `color: #1d4d51;
`    `}
.tab-content {
`        `display: none;
`    `}
.tab-content.active {
`        `display: block;
`    `}
</style>
{% endblock %}

{% block content %}

<div class="container mt-5">
`    `<!-- Вкладки навигации -->
`    `<ul class="nav" id="myTab" role="tablist">
`        `<li class="nav-item">
`            `<a class="nav-link" id="profile-tab" data-target="#profile">Профиль</a>
`        `</li>
`        `<li class="nav-item">
`            `<a class="nav-link active" id="orders-tab" data-target="#orders">Мои заказы</a>
`        `</li>
`        `<li class="nav-item">
`            `<a class="nav-link" href="{% url "user:logout" %}">Выйти</a>
`        `</li>
`    `</ul>

`    `<div class="tab-content active" id="orders">
`        `<div class="col-md-12">
`            `<div class="bg-white p-4 mb-4 mx-2 rounded custom-shadow mt-4">
`                `<h3 class="text-center mb-4">Мои заказы</h3>
`                `<div class="container">
`                    `<div class="accordion" id="accordionExample">
`                        `{% for order in orders %}
`                        `<div class="accordion-item">
`                            `<h2 class="accordion-header" id="heading{{ order.id }}">
`                                `<button class="accordion-button {% if order != orders.0 %}collapsed{% endif %}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{{ order.id }}" aria-expanded="false" aria-controls="collapse{{ order.id }}">
`                                    `Заказ № {{ order.id }} - {{ order.created\_timestamp }} | Статус: <strong class="mx-2">{{order.status}}</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;К оплате: <strong class="mx-2">{{order.orderitem\_set.all.total\_price}} P</strong>
`                                `</button>
`                            `</h2>
`                            `<div id="collapse{{ order.id }}" class="accordion-collapse collapse {% if order == orders.0 %}show{% endif %}" aria-labelledby="heading{{ order.id }}" data-bs-parent="#accordionExample">
`                                `<div class="accordion-body">
`                                    `{% for item in order.orderitem\_set.all %}
`                                    `<div class="row">
`                                        `<div class="col-1">
`                                            `<img src="{{ item.sizeproduct.product.image.url }}" alt="..." height="90px" width="65px">
`                                        `</div>
`                                        `<div class="col-6" style="padding-left: 30px">
`                                            `<h5 class="card-title mb-1">{{ item.sizeproduct.product.name }}</h5>
`                                            `<p style="margin-top:0; margin-bottom: 0; font-size: 15px">Размер: {{ item.sizeproduct.size.name }}</p>
`                                            `<p style="margin-top:0; margin-bottom: 0">Цвет: {% for color in item.sizeproduct.product.color.all %} {{ color.name }} {% endfor %}</p>
`                                            `<p class="mt-0">Состав: {% for consist in item.sizeproduct.product.consist.all %} {{ consist.name }} {% endfor %}</p>
`                                        `</div>
`                                        `<div class="col-5">
`                                            `<p>{{ item.price }} P&nbsp;&nbsp;&nbsp;x&nbsp;&nbsp;&nbsp;{{ item.quantity }}&nbsp;&nbsp;&nbsp;=&nbsp;&nbsp;&nbsp;{{ item.products\_price }} P</p>
`                                        `</div>
`                                    `</div>
`                                    `<hr>
`                                    `{% endfor %}
`                                `</div>
`                            `</div>
`                        `</div>
`                        `{% endfor %}
`                    `</div>
`                `</div>
`            `</div>
`        `</div>
`        `<div style="height: 350px"></div>
`    `</div>

`    `<!-- Содержимое вкладок -->
`    `<div class="tab-content-wrapper">
`        `<div class="tab-content" id="profile">
`            `<div class="bg-white p-4 mb-4 mx-2 rounded custom-shadow mt-4">
`                `<h3 class="text-center mb-4">Профиль пользователя</h3>
`                `<form action="{% url "users:profile" %}" method="post" enctype="multipart/form-data" novalidate>
`                    `{% csrf\_token %}
`                    `<div class="row">
`                        `<div class="col-md-12 mb-3">
`                            `<label for="id\_first\_name" class="form-label">Имя</label>
`                            `<input type="text" class="form-control" id="id\_first\_name" name="first\_name" placeholder="Введите ваше имя" value="{{ form.first\_name.value }}">
`                            `{% if form.first\_name.errors %}
`                            `<div style="color: red; margin-top: 5px;">{{form.first\_name.errors}}</div>
`                            `{% endif %}
`                        `</div>
`                        `<div class="col-md-12 mb-3">
`                            `<label for="id\_last\_name" class="form-label">Фамилия</label>
`                            `<input type="text" class="form-control" id="id\_last\_name" name="last\_name" placeholder="Введите вашу фамилию" value="{{ form.last\_name.value }}">
`                            `{% if form.last\_name.errors %}
`                            `<div style="color: red; margin-top: 5px;">{{form.last\_name.errors}}</div>
`                            `{% endif %}
`                        `</div>
`                        `<div class="col-md-12 mb-3">
`                            `<label for="id\_email" class="form-label">Email</label>
`                            `<input type="email" class="form-control" id="id\_email" name="email" placeholder="Введите ваш email \*youremail@example.com" value="{{ form.email.value }}">
`                            `{% if form.email.errors %}
`                            `<div style="color: red; margin-top: 5px;">{{form.email.errors}}</div>
`                            `{% endif %}
`                        `</div>
`                        `<div class="col-md-12 mb-3">
`                            `<label for="id\_phone\_number" class="form-label">Номер телефона</label>
`                            `<input type="text" class="form-control" id="id\_phone\_number" name="phone\_number" placeholder="Введите ваш номер телефона в формате: 8XXXXXXXXXX" value="{{ form.phone\_number.value }}">
`                            `{% if form.phone\_number.errors %}
`                            `<div style="color: red; margin-top: 5px;">{{form.phone\_number.errors}}</div>
`                            `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row mt-2">
`                        `<div class="col-10">
`                        `</div>
`                        `<div class="col-2">
`                            `<button type="submit" name="profile\_submit" class="btn btn-dark" style="background-color: #1d4d51; color: #e1d89f">Сохранить</button>
`                        `</div>
`                    `</div>
`                `</form>
`                `<hr>
`                `<h3 class="text-center mb-4 mt-3">Изменение пароля</h3>
`                `<form action="{% url "users:profile" %}" method="post">
`                    `{% csrf\_token %}
`                    `<div class="row">
`                      `<div class="col-md-12 mb-3">
`                            `<label for="id\_old\_password" class="form-label">Старый пароль</label>
`                            `<input type="password" class="form-control" id="id\_old\_password" name="old\_password" placeholder="Введите старый пароль" value="">
`                            `{% if password\_form.old\_password.errors %}
`                            `<div style="color: red; margin-top: 5px;">{{ password\_form.old\_password.errors }}</div>
`                            `{% endif %}
`                        `</div>
`                        `<div class="col-md-12 mb-3">
`                            `<label for="id\_new\_password1" class="form-label">Новый пароль</label>
`                            `<input type="password" class="form-control" id="id\_new\_password1" name="new\_password1" placeholder="Введите новый пароль" value="">
`                            `{% if password\_form.new\_password1.errors %}
`                            `<div style="color: red; margin-top: 5px;">{{ password\_form.new\_password1.errors }}</div>
`                            `{% endif %}
`                        `</div>
`                        `<div class="col-md-12 mb-3">
`                            `<label for="id\_new\_password2" class="form-label">Подтверждение нового пароля</label>
`                            `<input type="password" class="form-control" id="id\_new\_password2" name="new\_password2" placeholder="Подтвердите новый пароль" value="">
`                            `{% if password\_form.new\_password2.errors %}
`                            `<div style="color: red; margin-top: 5px;">{{ password\_form.new\_password2.errors }}</div>
`                            `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row mt-2">
`                        `<div class="col-10">
`                        `</div>
`                        `<div class="col-2">
`                            `<button type="submit" name="password\_submit" class="btn btn-dark" style="background-color: #1d4d51; color: #e1d89f">Сохранить</button>
`                        `</div>
`                    `</div>
`                `</form>
`            `</div>
`        `</div>
`    `</div>
</div>

<script>
`    `document.addEventListener('DOMContentLoaded', function() {
`        `const tabs = document.querySelectorAll('.nav-link');
`        `const contents = document.querySelectorAll('.tab-content');

`        `tabs.forEach(tab => {
`            `tab.addEventListener('click', function() {
`                `tabs.forEach(t => t.classList.remove('active'));
`                `contents.forEach(c => c.classList.remove('active'));

`                `tab.classList.add('active');
`                `document.querySelector(tab.dataset.target).classList.add('active');
`            `});
`        `});
`    `});
</script>

{% endblock %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/templates/users/forgot\_password.html**
{% extends "base.html" %}
{% load static %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block content %}
<div class="row">
`    `<div class="container mt-5">
`        `<div class="row justify-content-center">
`            `<div class="col-md-6 bg-white p-4 mb-4 mx-3 rounded custom-shadow">
`                `<h2 class="text-center mb-4" style="color: #1d4d51">Восстановить логин или пароль</h2>
`                `<form action="{% url "user:forgot\_password" %}" method="post" novalidate id="forgotForm">
`                    `{% csrf\_token %}
`                    `{{ form.non\_field\_errors }}
`                    `<div class="form-group mb-3">
`                        `<label for="id\_email" class="form-label">Email\*</label>
`                        `<input type="email" class="form-control"
`                        `value=""
`                        `name="email" id="id\_email"
`                        `placeholder="Введите email от вашего аккаунта"
`                        `required>
`                        `<div style="color: red" id="emailError"></div>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-7">
`                            `<button type="submit" class="btn btn-block mt-2 mb-3" style="background-color: #1d4d51; color: #a18c0d">Отправить письмо на почту</button>
`                        `</div>
`                    `</div>
`                `</form>
`            `</div>
`        `</div>
`    `</div>
`    `<div style="height: 200px"></div>
</div>
<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
`    `<script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
`    `<!-- Подключаем Bootstrap JS -->
`    `<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
`    `<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script>
`    `$(document).ready(function() {
`        `$('#forgotForm').on('submit', function(event) {
`            `let valid = true;
`            `let email = $('#id\_email');
`            `let emailError = $('#emailError');

`            `if (email.val() === '') {
`                `valid = false;
`                `emailError.text('Введите электронную почту.');
`            `} else {
`                `emailError.text('');
`            `}

`            `if (!valid) {
`                `event.preventDefault();
`            `}
`        `});
`    `});
</script>
{% endblock %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/templates/users/users\_cart.html**
{% extends "base.html" %}
{% load static %}
{% load carts\_tags %}


{% block content %}
{% user\_carts request as carts %}
<div class="row">
`    `<div class="container mt-5">
`        `<div class="row justify-content-center">
`            `<div class=" bg-white p-4 mb-4 mx-2 rounded custom-shadow">
`                `<h3 class="text-center mb-4">Корзина</h3>
`                `<div class="container" id="cart-items-container">
`                    `<!-- Разметка корзины -->
`                    `{% include "carts/includes/included\_cart.html" %}
`                    `<!-- Закончилась разметка корзины -->
`                `</div>
`            `</div>
`        `</div>
`    `</div>
</div>
{% endblock  %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/templates/users/login.html**
{% extends "base.html" %}
{% load static %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block content %}
<div class="row">
`    `<div class="container mt-5">
`        `<div class="row justify-content-center">
`            `<div class="col-md-6 bg-white p-4 mb-4 mx-3 rounded custom-shadow">
`                `<h2 class="text-center mb-4" style="color: #1d4d51">Авторизация</h2>
`                `<form  action="{% url "user:login" %}" method="post" novalidate>
`                    `{% csrf\_token %}
`                    `{% if request.GET.next %}
`                        `<input type="hidden" name="next" value={{request.GET.next}}>
`                    `{% endif %}
`                    `<div class="mb-3">
`                        `<label for="id\_username" class="form-label">Логин</label>
`                        `<input type="text" class="form-control"
`                        `value="{% if form.username.value %}{{ form.username.value }}{% endif %}"
`                        `name="username" id="id\_username"
`                        `placeholder="Введите ваш логин"
`                        `required>
`                    `</div>
`                    `<div class="mb-3">
`                        `<label for="id\_password" class="form-label">Пароль</label>
`                        `<input type="password" class="form-control" name="password" id="id\_password"
`                        `placeholder="Введите ваш пароль" required>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-3">
`                            `<button type="submit" class="btn btn-block mt-3 mb-5 " style="background-color: #1d4d51; color: #a18c0d">Войти</button>
`                        `</div>
`                        `<div class="col-9">
`                            `<div class="mt-4">
`                                `<a href="{% url "user:forgot\_password" %}">Забыли логин или пароль?</a> | <a href="{% url "user:registration" %}">Создать аккаунт</a>
`                            `</div>
`                        `</div>
`                    `</div>
`                `</form>
`            `</div>
`        `</div>
`    `</div>
`    `<div style="height: 200px"></div>
</div>
{% endblock  %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/users/templates/users/registration.html**
{% extends "base.html" %}
{% load static %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block content %}
<div class="row">
`    `<div class="container mt-2">
`        `<div class="row justify-content-center">
`            `<div class="col-md-6 bg-white p-4 mb-5 mx-2 rounded custom-shadow">
`                `<h2 class="text-center mb-4" style="color: #1d4d51;">Регистрация</h2>
`                `<form action="{% url "user:registration" %}" method="post" novalidate>
`                    `{% csrf\_token %}
`                    `<div class="row">
`                        `<div class="col-md-11 mb-3">
`                            `<label for="id\_first\_name" class="form-label">Имя\*</label>
`                            `<input type="text" class="form-control" id="id\_first\_name"
`                                `value="{% if form.first\_name.value %}{{ form.first\_name.value }}{% endif %}"
`                                `name="first\_name"
`                                `placeholder="Введите имя" required>
`                                `{% if form.first\_name.errors %}
`                                `<div class="alert alert-danger alert-dismissible fade show mt-2">{{form.first\_name.errors}}</div>
`                                `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-md-11 mb-3">
`                            `<label for="id\_last\_name" class="form-label">Фамилия\*</label>
`                            `<input type="text" class="form-control" id="id\_last\_name"
`                                `value="{% if form.last\_name.value %}{{ form.last\_name.value }}{% endif %}"
`                                `name="last\_name"
`                                `placeholder="Введите фамилию" required>
`                                `{% if form.last\_name.errors %}
`                                `<div class="alert alert-danger alert-dismissible fade show mt-2">{{form.last\_name.errors}}</div>
`                                `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-md-11 mb-3">
`                            `<label for="id\_username" class="form-label">Логин\*</label>
`                            `<input type="text" class="form-control" id="id\_username"
`                                `value="{% if form.username.value %}{{ form.username.value }}{% endif %}"
`                                `name="username"
`                                `placeholder="Введите логин" required>
`                                `{% if form.username.errors %}
`                                `<div class="alert alert-danger alert-dismissible fade show mt-2">{{form.username.errors}}</div>
`                                `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-md-11 mb-3">
`                            `<label for="id\_email" class="form-label">Email\*</label>
`                            `<input type="email" class="form-control" id="id\_email"
`                                `value="{% if form.email.value %}{{ form.email.value }}{% endif %}"
`                                `name="email"
`                                `placeholder="Введите email" required>
`                                `{% if form.email.errors %}
`                                `<div class="alert alert-danger alert-dismissible fade show mt-2">{{form.email.errors}}</div>
`                                `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-md-11 mb-3">
`                            `<label for="id\_phone\_number" class="form-label">Номер телефона\*</label>
`                            `<input type="text" class="form-control" id="id\_phone\_number"
`                                `value="{% if form.phone\_number.value %}{{ form.phone\_number.value }}{% endif %}"
`                                `name="phone\_number"
`                                `placeholder="Введите номер телефона в формате: 8XXXXXXXXXX" required>
`                                `{% if form.phone\_number.errors %}
`                                    `<div class="alert alert-danger alert-dismissible fade show mt-2">{{form.phone\_number.errors}}</div>
`                                `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-md-11 mb-3">
`                            `<label for="id\_password1" class="form-label">Пароль\*</label>
`                            `<input type="password" class="form-control" id="id\_password1"
`                                `value="{% if form.password1.value %}{{ form.password1.value }}{% endif %}"
`                                `name="password1"
`                                `placeholder="Введите пароль" required>
`                                `{% if form.password1.errors %}
`                                `<div class="alert alert-danger alert-dismissible fade show mt-2">{{form.password1.errors}}</div>
`                                `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-md-11 mb-3">
`                            `<label for="id\_password2" class="form-label">Подтверждение пароля\*</label>
`                            `<input type="password" class="form-control" id="id\_password2"
`                                `value="{% if form.password2.value %}{{ form.password2.value }}{% endif %}"
`                                `name="password2"
`                                `placeholder="Подтвердите пароль" required>
`                                `{% if form.password2.errors %}
`                                `<div class="alert alert-danger alert-dismissible fade show mt-2">{{form.password2.errors}}</div>
`                                `{% endif %}
`                        `</div>
`                    `</div>
`                    `<div class="row justify-content-center">
`                        `<div class="col-md-4">
`                            `<button type="submit"
`                            `class="btn btn-dark btn-block mt-2" style="background-color: #1d4d51; color: #a18c0d; margin-left: -10px">Зарегистрироваться</button>
`                        `</div>
`                    `</div>
`                `</form>
`            `</div>
`        `</div>
`    `</div>
</div>
{% endblock  %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/templates/base.html**
{% load static %}
{% load goods\_tags %}

<!DOCTYPE html>
<html lang="en">

<head>
`    `<meta charset="UTF-8">
`    `<meta http-equiv="X-UA-Compatible" content="IE=edge">
`    `<meta name="viewport" content="width=device-width, initial-scale=1.0">
`    `<link rel="stylesheet" href="{% static "deps/css/bootstrap/bootstrap.min.css" %}">
`    `{% block css %}

`    `{% endblock %}
`    `<!-- Favicons for different platforms -->
`    `<link rel="apple-touch-icon" sizes="180x180" href="{% static "deps/images/passag.jpeg" %}">
`    `<link rel="icon" type="image/png" sizes="32x32" href="{% static "deps/images/passag.jpeg" %}">
`    `<link rel="icon" type="image/png" sizes="16x16" href="{% static "deps/images/passag.jpeg" %}">
`    `<link rel="manifest" href="{% static "deps/favicon/site.webmanifest" %}">
`    `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/assets/owl.carousel.min.css" integrity="sha512-tS3S5qG0BlhnQROyJXvNjeEM4UpMXHrQfTGmbQ1gKmelCxlSEBUaxhRBj/EFTzpbP4RVSrpEikbmdJobCvhE3g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
`    `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/assets/owl.theme.default.css" integrity="sha512-OTcub78R3msOCtY3Tc6FzeDJ8N9qvQn1Ph49ou13xgA9VsH9+LRxoFU6EqLhW4+PKRfU+/HReXmSZXHEkpYoOA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
`    `<link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons" rel="stylesheet">

`    `<title>{{ title }}</title>
`    `<style>
.card1 {
`            `background-color: #e1d89f;
`            `padding: 20px;
`            `margin-bottom: 20px;
`        `}
.card1 button {
`            `display: block;
`            `width: 100%;
`            `padding: 10px;
`            `margin-bottom: 10px;
`            `background-color: #1d4d51;
`            `color: #a18c0d;
`            `border: none;
`            `border-radius: 5px;
`            `cursor: pointer;
`        `}
.card1 button:hover {
`            `background-color: #216268;
`        `}
.rte {
`            `background-color: #e1d89f;
`        `}

.my-custom-tooltip .tooltip-inner {
`        `background-color: rgba(0, 0, 0, 0.8); /\* Цвет фона подсказки \*/
`        `color: #fff; /\* Цвет текста подсказки \*/
`        `border-radius: 4px; /\* Радиус скругления углов \*/
`        `opacity: 0.9; /\* Прозрачность подсказки \*/
`    `}

`        `body {
`            `header {
`                `nav {
`                    `background-color: #1d4d51;
`                    `div {
`                        `a {
`                            `img {
`                                `max-height: 35px;
`                            `}
`                        `}
`                        `div {
`                            `form {
`                                `input {
`                                    `background-color: #a18c0d;
`                                `}
`                            `}
`                        `}
`                    `}
`                `}
`            `}
`            `footer {
`                `background-color: #1d4d51;
`            `}
`        `}

`    `</style>
</head>

<body class="rte">
`    `<header class="fixed-top">
`        `<nav class="navbar navbar-expand-lg">
`            `<div class="container d-flex" style="justify-content: normal">
`                `<a class="navbar-brand" href="{% url "main:index" %}" data-toggle="tooltip" data-placement="bottom" title="На главную">
`                    `<img src="/static/deps/images/passag2.jpeg">
`                `</a>
`                `<div class="flex-grow-1"></div>
`                    `{% if user.is\_admin or user.is\_staff %}
`                        `<a href="{% url "main:panel" %}" class="mt-1" style="margin-right: 20px;" data-toggle="tooltip" data-placement="bottom" title="Панель администратора">
`                            `<img class="mx-1" src="{% static "deps/icons/setting.svg" %}"
`                                `alt="Catalog Icon" width="32" height="32">
`                        `</a>
`                    `{% endif %}
`                    `{% block modal\_cart %}{% endblock  %}
`                    `{% if not user.is\_authenticated %}
`                        `<a href="{% url "user:login" %}" type="submit" class="mt-1 " style="margin-right: 20px;" data-toggle="tooltip" data-placement="bottom" title="Авторизироваться">
`                            `<img class="mx-1" src="{% static "deps/icons/profile-ohr.svg" %}"
`                                `alt="Catalog Icon" width="28" height="28">
`                        `</a>
`                    `{% else %}
`                        `<a href="{% url "user:profile" %}" type="submit" class="mt-1 " style="margin-right: 20px;" data-toggle="tooltip" data-placement="bottom" title="Профиль">
`                            `<img class="mx-1" src="{% static "deps/icons/profile-ohr.svg" %}"
`                                `alt="Catalog Icon" width="28" height="28">
`                        `</a>
`                    `{% endif %}
`                    `<a href="{% url "main:about" %}" class="mt-1" style="margin-right: 20px;" data-toggle="tooltip" data-placement="bottom" title="О нас">
`                        `<img class="mx-1" src="{% static "deps/icons/location-ohr.svg" %}"
`                            `alt="Catalog Icon" width="28" height="28">
`                    `</a>
`                    `<form style="justify-self: end" class="d-flex" role="search" action="{% url "catalog:search" %}" method="get" autocomplete="off" onsubmit="return validateForm()">
`                        `<input id="searchInput" class="me-2 form-control input-ohr" type="search" name="q" placeholder="Поиск" aria-label="Search" autocomplete="off" oninput="toggleButton()">
`                        `<button id="searchButton" class="btn" type="submit" data-toggle="tooltip" data-placement="bottom" title="Поиск" disabled>
`                            `<img class="mx-1" src="{% static "deps/icons/search-ohr.svg" %}" alt="Catalog Icon" width="28" height="28">
`                        `</button>
`                    `</form>
`                `</div>
`            `</div>
`        `</nav>
`    `</header>
`    `<section>
`        `<div class="container">
`            `<!-- Каталог и корзина с фиксированным расположением на странице -->

`            `<div class="row mt-1 card1 position-fixed" style=" position: absolute; left: 30px; top: 100px; width: 250px; border: none; overflow-x: scroll;">
`                    `{% tag\_categories as categories %}
`                    `{% for category in categories %}
`                        `<a href="{% url "catalog:index" category.slug %}" style="display: block; text-decoration: none"><button>{{category.name}}</button></a>
`                    `{% endfor %}
`            `</div>
`        `</div>
`        `<!-- Контент -->
`        `<div class="container" style="flex: 1">
`            `<div class="row mt-1">
`                `<div class="col-lg-2">
`                    `<!-- Пустой блок на Ваше усмотрение -->
`                `</div>
`                `<div class="col-lg-10" style="margin-top: 70px">
`                    `<!-- Контент на странице -->
`                    `{% include "includes/notifications.html" %}
`                    `{% block content %}{% endblock %}
`                `</div>
`            `</div>

`        `</div>
`    `</section>

`    `<div class="py-4" style="background-color: #1d4d51; margin-top: 60px">
`        `<div class="container d-flex" style="justify-content: space-between">
`            `<div style="color: #a18c0d">
`                `<p class="h4" style="margin-bottom: 10px; padding-left: 30px">Каталог</p>
`                `<ul>
`                    `{% tag\_categories as categories %}
`                    `{% for category in categories %}
`                        `<li style="list-style-type: none"><a class="link-warning link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover" style="color: #a18c0d !important;" href="{% url "catalog:index" category.slug %}">{{category.name}}</a></li>
`                    `{% endfor %}
`                `</ul>
`            `</div>
`            `<div style="color: #a18c0d; margin-left: 60px">
`                `<p class="h4" style="margin-bottom: 10px;">О компании</p>
`                `<p style="margin-bottom: 0"><a class="link-warning link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover" style="color: #a18c0d !important;" href="{% url "main:about" %}">О нас</a></p>
`            `</div>
`            `<div class="ms-auto" style="color: #a18c0d">
`                `<p class="h4" style="margin-bottom: 10px;">Контакты</p>
`                `<p style="margin-bottom: 0">Телефон: +7 (950) 700-66-48</p>
`                `<p style="margin-bottom: 0">Email: passag@mail.ru</p>
`                `<p style="margin-bottom: 0">Адрес: ул. Улица Октябрьской Революции, 23, город Смоленск</p>
`                `<p class="h4" style="margin-bottom: 10px; margin-top: 30px;">Мы в соцсетях</p>
`                `<a href="https://vk.com/passagesm">
`                    `<img class="mx-1" src="{% static "deps/icons/vk-ohr.svg" %}"
`                        `alt="Catalog Icon" width="28" height="28">
`                `</a>
`            `</div>
`        `</div>
`    `</div>

`    `<script src="{% static "deps/js/jquery/jquery-3.7.0.min.js" %}"></script>
`    `<script src="{% static "deps/js/jquery-ajax.js" %}"></script>
`    `<script src="{% static "deps/js/bootstrap/bootstrap.bundle.min.js" %}"></script>
`    `<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js" integrity="sha512-v2CJ7UaYy4JwqLDIrZUI/4hqeoQieOmAZNXBeQyjo21dadnwR+8ZaIJVT8EE2iyI61OV8e6M8PP2/4hpQINQ/g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
`    `<script src="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/owl.carousel.min.js" integrity="sha512-bPs7Ae6pVvhOSiIcyUClR7/q2OAsRiovw4vAkX+zJbw3ShAeeqezq50RIIcIURq7Oa20rW2n2q+fyXBNcU9lrw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
`    `<script>
`        `$(document).ready(function(){
`          `$(".owl-carousel").owlCarousel({
`                `items:1,
`                `loop:true,
`                `margin:10,
`                `autoplay:true,
`                `autoplayTimeout:5000,
`                `autoplayHoverPause:true
`            `});
`            `$('.play').on('click',function(){
`                `owl.trigger('play.owl.autoplay',[1000])
`            `})
`            `$('.stop').on('click',function(){
`                `owl.trigger('stop.owl.autoplay')
`            `});
`            `});
`        `$(document).ready(function(){
`            `$('[data-toggle="tooltip"]').tooltip({
`                `placement: 'bottom',
`                `template: '<div class="tooltip my-custom-tooltip" role="tooltip"><div class="tooltip-inner"></div></div>'// Устанавливаем расположение tooltips снизу
`            `});
`        `});
`        `function toggleButton() {
`            `var input = document.getElementById('searchInput');
`            `var button = document.getElementById('searchButton');
`            `button.disabled = input.value.trim() === '';
`        `}

`        `function validateForm() {
`            `var input = document.getElementById('searchInput').value.trim();
`            `if (input === '') {
`                `// Предотвращаем отправку формы, если поле поиска пустое
`                `return false;
`            `}
`            `return true;
`        `}
`    `</script>

</body>

</html>
## **Файл: /Users/katedem/PycharmProjects/shop-passag/templates/includes/notifications.html**
{% load static %}

{% if form.non\_field\_errors %}
`    `<div class="container mt-4">
`        `<div class="row justify-content-center">
`            `<div class="col-md-6">
`                `<div class="alert alert-danger alert-dismissible fade show custom-shadow" role="alert">
`                    `{{form.non\_field\_errors}}
`                    `<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
`                `</div>
`            `</div>
`        `</div>
`    `</div>
{% endif %}

<div class="container mt-4">
`    `<div class="row justify-content-center">
`        `<div class="col-md-6">
`            `{% if messages %}
`                `{% for message in messages %}
`                    `{% if message.tags == 'success' %}
`                    `<div id="notification" class="position-fixed start-50 translate-middle-x z-3 alert alert-success fade show custom-shadow" role="alert">
`                        `{{ message }}
`                    `</div>
`                    `{% endif %}
`                    `{% if message.tags == 'warning' %}
`                    `<div id="notification" class="position-fixed start-50 translate-middle-x z-3 alert alert-danger fade show custom-shadow" role="alert">
`                        `{{ message }}
`                    `</div>
`                    `{% endif %}
`                `{% endfor %}
`            `{% else %}
`            `<div id="jq-notification" class="position-fixed start-50 translate-middle-x z-3 alert alert-success fade show custom-shadow" style="display: none;" role="alert">
`            `</div>
`            `{% endif %}
`        `</div>
`    `</div>
</div>
## **Файл: /Users/katedem/PycharmProjects/shop-passag/templates/includes/cart\_button.html**
{% load static %}
{% load carts\_tags %}

{% user\_carts request as carts %}

<div>
`    `<a type="button" id="modalButton">
`        `<img class="mx-1" src="{% static "deps/icons/basket2-fill-ohr.svg" %}"
`            `alt="Catalog Icon" width="28" height="28" data-toggle="tooltip" title="Корзина">
`        `<span id="goods-in-cart-count" style="color: #a18c0d; margin-right: 20px;">{{ carts.total\_quantity }}</span>
`    `</a>
{#    <span id="goods-in-cart-count" style="color: #a18c0d">{{ carts.total\_quantity }}</span>#}
{#    <button type="button" class="btn btn-dark btn-secondary d-flex" id="modalButton"#}
{#        aria-expanded="false">#}
{#        <img class="mx-1" src="{% static "deps/icons/basket2-fill-ohr.svg" %}" alt="Catalog Icon" width="24"#}
{#            height="24">#}
{#        <span id="goods-in-cart-count" style="color: #a18c0d">{{ carts.total\_quantity }}</span>#}
{#    </button>#}
</div>
<!-- Разметка модального окна корзины -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel"
`    `aria-hidden="true">
`    `<div class="modal-dialog modal-dialog-scrollable">
`        `<div class="modal-content">
`            `<div class="modal-header" style="border: none; margin-top: 10px; margin-right: 10px">
`                `<button type="button" class="btn-close" data-bs-dismiss="modal"
`                    `aria-label="Close"></button>
`            `</div>
`            `<div class="modal-body">
`                `<h3 class="text-center mb-4" style="color: #1d4d51; margin-top: -20px">Корзина</h3>
`                `<div class="container" id="cart-items-container">
`                    `<!-- Разметка корзины -->
`                    `{% include "carts/includes/included\_cart.html" %}
`                    `<!-- Закончилась разметка корзины -->
`                `</div>
`            `</div>
`        `</div>
`    `</div>
</div>
## **Файл: /Users/katedem/PycharmProjects/shop-passag/fixtures/goods/cats.json**
[
`  `{
`    `"model": "goods.categories",
`    `"pk": 4,
`    `"fields": {
`      `"name": "Все товары",
`      `"slug": "all"
`    `}
`  `},
`  `{
`    `"model": "goods.categories",
`    `"pk": 5,
`    `"fields": {
`      `"name": "Кухня",
`      `"slug": "kuhnya"
`    `}
`  `},
`  `{
`    `"model": "goods.categories",
`    `"pk": 6,
`    `"fields": {
`      `"name": "Спальня",
`      `"slug": "spalnya"
`    `}
`  `},
`  `{
`    `"model": "goods.categories",
`    `"pk": 7,
`    `"fields": {
`      `"name": "Декор",
`      `"slug": "dekor"
`    `}
`  `},
`  `{
`    `"model": "goods.categories",
`    `"pk": 8,
`    `"fields": {
`      `"name": "Гостинная",
`      `"slug": "gostinnaya"
`    `}
`  `},
`  `{
`    `"model": "goods.categories",
`    `"pk": 9,
`    `"fields": {
`      `"name": "Офис",
`      `"slug": "ofis"
`    `}
`  `},
`  `{
`    `"model": "goods.categories",
`    `"pk": 10,
`    `"fields": {
`      `"name": "Фурнитура",
`      `"slug": "furnitura"
`    `}
`  `}
]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/fixtures/goods/prod.json**
[{"model": "goods.products", "pk": 1, "fields": {"name": "Чайный столик и три стула", "slug": "chajnyj-stolik-i-tri-stula", "description": "Комплект из трёх стульев и дизайнерский столик для гостинной комнаты.", "image": "goods\_images/set\_of\_tea\_table\_and\_three\_chairs.jpg", "price": "150.00", "discount": "10.00", "quantity": 10, "category": 5}}, {"model": "goods.products", "pk": 2, "fields": {"name": "Чайный столик и два стула", "slug": "chajnyj-stolik-i-dva-stula", "description": "Набор из стола и двух стульев в минималистическом стиле.", "image": "goods\_images/set\_of\_tea\_table\_and\_two\_chairs.jpg", "price": "93.00", "discount": "2.50", "quantity": 5, "category": 5}}, {"model": "goods.products", "pk": 3, "fields": {"name": "Двухспальная кровать", "slug": "dvuhspalnaya-krovat", "description": "Кровать двухспальная с надголовником и вообще очень ортопедичная.", "image": "goods\_images/double\_bed.jpg", "price": "670.00", "discount": "0.00", "quantity": 7, "category": 6}}, {"model": "goods.products", "pk": 4, "fields": {"name": "Кухонный стол с раковиной", "slug": "kuhonnyj-stol-s-rakovinoj", "description": "Кухонный стол для обеда с встроенной раковиной и стульями.", "image": "goods\_images/kitchen\_table\_PFsm2Fr.jpg", "price": "365.00", "discount": "0.00", "quantity": 12, "category": 5}}, {"model": "goods.products", "pk": 5, "fields": {"name": "Кухонный стол с встройкой", "slug": "kuhonnyj-stol-s-vstrojkoj", "description": "Кухонный стол со встроенной плитой и раковиной. Много полок и вообще красивый.", "image": "goods\_images/kitchen\_table\_2\_C6dHEMj.jpg", "price": "430.00", "discount": "4.99", "quantity": 9, "category": 5}}, {"model": "goods.products", "pk": 6, "fields": {"name": "Угловой диван для гостинной", "slug": "uglovoj-divan-dlya-gostinnoj", "description": "Угловой диван, раскладывается в двухспальную кровать, для гостинной и приема гостей самое то!", "image": "goods\_images/corner\_sofa.jpg", "price": "610.00", "discount": "2.00", "quantity": 8, "category": 8}}, {"model": "goods.products", "pk": 7, "fields": {"name": "Прикроватный столик", "slug": "prikrovatnyj-stolik", "description": "Прикроватный столик с двумя выдвижными ящиками (цветок не входит в комплект).", "image": "goods\_images/bedside\_table.jpg", "price": "55.00", "discount": "0.00", "quantity": 5, "category": 6}}, {"model": "goods.products", "pk": 8, "fields": {"name": "Диван обыкновенный", "slug": "divan-obyknovennyj", "description": "Диван, он же софа обыкновенная, ничего примечательного для описания.", "image": "goods\_images/sofa.jpg", "price": "190.00", "discount": "4.99", "quantity": 7, "category": 8}}, {"model": "goods.products", "pk": 9, "fields": {"name": "Стул офисный", "slug": "stul-ofisnyj", "description": "Описание товара, про то какой он классный, но это стул, что тут сказать...", "image": "goods\_images/office\_chair.jpg", "price": "30.00", "discount": "0.50", "quantity": 40, "category": 9}}, {"model": "goods.products", "pk": 10, "fields": {"name": "Растение", "slug": "rastenie", "description": "Растение для украшения вашего интерьера подарит свежесть и безмятежность обстановке.", "image": "goods\_images/plants.jpg", "price": "10.00", "discount": "0.00", "quantity": 17, "category": 7}}, {"model": "goods.products", "pk": 11, "fields": {"name": "Цветок стилизированный", "slug": "cvetok-stilizirovannyj", "description": "Дизайнерский цветок (возможно искусственный) для украшения интерьера.", "image": "goods\_images/flower.jpg", "price": "15.00", "discount": "0.00", "quantity": 17, "category": 7}}, {"model": "goods.products", "pk": 12, "fields": {"name": "Прикроватный столик 2", "slug": "prikrovatnyj-stolik-2", "description": "Столик, довольно странный на вид, но подходит для размещения рядом с кроватью.", "image": "goods\_images/strange\_table.jpg", "price": "25.00", "discount": "90.00", "quantity": 10, "category": 6}}]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/models.py**
from django.db import models
from django.urls import reverse
\# from django.contrib.postgres.fields import CITextField


class SizeProductQueryset(models.QuerySet):

`    `def total\_count(self):
`        `if self:
`            `return sum(sizeproduct.count for sizeproduct in self)
`        `return 0


class Categories(models.Model):
`    `name = models.CharField(max\_length=150, unique=True, verbose\_name='Название')
`    `slug = models.SlugField(max\_length=200, unique=True, blank=True, null=True, verbose\_name='URL')
`    `tnved = models.CharField(max\_length=150, verbose\_name='Код тн вэд', null=True)
`    `filter\_size = models.BooleanField(verbose\_name='Нужен фильтр для размеров', default=True)
`    `filter\_consist = models.BooleanField(verbose\_name='Нужен фильтр для составов', default=True)

`    `class Meta:
`        `db\_table = 'category'
`        `verbose\_name = 'Категорию'
`        `verbose\_name\_plural = 'Категории'
`        `ordering = ("id",)

`    `def \_\_str\_\_(self):
`        `return self.name


class Sizes(models.Model):
`    `"""Размер товара"""

`    `RUSSIAN = 1
`    `INTERNATIONAL = 2

`    `SIZE\_TYPE = [
`        `(RUSSIAN, 'РОССИЯ'),
`        `(INTERNATIONAL, 'МЕЖДУНАРОДНЫЙ'),
`    `]

`    `name = models.TextField(help\_text='Название')
`    `type = models.PositiveSmallIntegerField(choices=SIZE\_TYPE, default=RUSSIAN)

`    `class Meta:
`        `verbose\_name = 'Размер'
`        `verbose\_name\_plural = 'Размеры'
`        `ordering = ('id',)

`    `def \_\_str\_\_(self):
`        `return self.name


class Color(models.Model):
`    `"""Цвет товара"""

`    `name = models.TextField(help\_text='Название')
`    `hex = models.TextField(help\_text='Цвет в формате hex', null=True)

`    `class Meta:
`        `verbose\_name = 'Цвет'
`        `verbose\_name\_plural = 'Цвета'
`        `ordering = ('id',)

`    `def \_\_str\_\_(self):
`        `return self.name


class Consist(models.Model):
`    `"""Состав товара"""

`    `name = models.TextField(help\_text='Название')

`    `class Meta:
`        `verbose\_name = 'Состав'
`        `verbose\_name\_plural = 'Составы'
`        `ordering = ('id',)

`    `def \_\_str\_\_(self):
`        `return self.name


class Country(models.Model):
`    `"""Цвет товара"""

`    `name = models.TextField(help\_text='Название')

`    `class Meta:
`        `verbose\_name = 'Строна производства'
`        `verbose\_name\_plural = 'Строна производства'
`        `ordering = ('id',)

`    `def \_\_str\_\_(self):
`        `return self.name


class Products(models.Model):
`    `name = models.TextField(max\_length=150, verbose\_name='Название')
`    `slug = models.SlugField(max\_length=200, unique=True, blank=True, null=True, verbose\_name='URL')
`    `description = models.TextField(blank=True, null=True, verbose\_name='Описание')
`    `image = models.ImageField(upload\_to='goods\_images', blank=True, null=True, verbose\_name='Изображение')
`    `price = models.DecimalField(default=0.00, max\_digits=7, decimal\_places=2, verbose\_name='Цена')
`    `discount = models.DecimalField(default=0.00, max\_digits=4, decimal\_places=2, verbose\_name='Скидка в %')
`    `category = models.ForeignKey(to=Categories, on\_delete=models.SET\_NULL, verbose\_name='Категория', null=True)
`    `article = models.PositiveIntegerField(default=0, help\_text='Артикул товара', unique=True)
`    `created\_at = models.DateField(auto\_now\_add=True, help\_text='Дата добавления', null=True)

`    `size = models.ManyToManyField(Sizes, through='SizeProductRelation')
`    `consist = models.ManyToManyField(Consist, related\_name='consist')
`    `color = models.ManyToManyField(Color, related\_name='color')
`    `country = models.ForeignKey(to=Country, on\_delete=models.SET\_NULL, verbose\_name='Страна производства', null=True)


`    `class Meta:
`        `db\_table = 'product'
`        `verbose\_name = 'Продукт'
`        `verbose\_name\_plural = 'Продукты'
`        `ordering = ("id",)

`    `def \_\_str\_\_(self):
`        `return f'{self.name} {self.article}'

`    `def get\_absolute\_url(self):
`        `return reverse('catalog:product', kwargs={'product\_slug': self.slug})

`    `def display\_id(self):
`        `return f"{self.id:05}"

`    `def sell\_price(self):
`        `if self.discount:
`            `return round(self.price - self.price \* self.discount / 100, 2)

`        `return self.price


class SizeProductRelation(models.Model):
`    `"""Количество товаров размера"""

`    `product = models.ForeignKey(Products, on\_delete=models.CASCADE)
`    `size = models.ForeignKey(Sizes, on\_delete=models.CASCADE)
`    `count = models.PositiveIntegerField(default=0, help\_text='Количество')

`    `class Meta:
`        `verbose\_name = 'Количество товара размера'
`        `verbose\_name\_plural = 'Количество товара размера'

`    `objects = SizeProductQueryset().as\_manager()

`    `def \_\_str\_\_(self):
`        `return f"{self.count} {self.size.name} {self.product.name}"
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/\_\_init\_\_.py**

## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/apps.py**
from django.apps import AppConfig


class GoodsConfig(AppConfig):
`    `default\_auto\_field = 'django.db.models.BigAutoField'
`    `name = 'goods'
`    `verbose\_name='Товары'
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/admin.py**
from django.contrib import admin

from goods.models import Categories, Products, Sizes, Color, Consist, SizeProductRelation, Country


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
`    `list\_display = ["name"]
`    `search\_fields = ["name"]
`    `ordering = ["id"]


@admin.register(SizeProductRelation)
class SizeProductRelationAdmin(admin.ModelAdmin):
`    `list\_display = ["product", "size", "count"]
`    `list\_filter = ["product", "size", "count"]
`    `search\_fields = ["product", "size"]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
`    `list\_display = ["name",]
`    `search\_fields = ["name"]
`    `ordering = ["id"]


@admin.register(Consist)
class ConsistAdmin(admin.ModelAdmin):
`    `list\_display = ["name",]
`    `search\_fields = ["name"]
`    `ordering = ["id"]


@admin.register(Country)
class ConsistAdmin(admin.ModelAdmin):
`    `list\_display = ["name", ]
`    `search\_fields = ["name"]
`    `ordering = ["id"]


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
`    `prepopulated\_fields = {"slug": ("name",)}
`    `list\_display = ["name"]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
`    `prepopulated\_fields = {"slug": ("name", "article")}
`    `list\_display = ["name", "price", "discount", "created\_at"]
`    `list\_editable = ["discount"]
`    `search\_fields = ["name", "article"]
`    `list\_filter = ["discount", "category"]
`    `fields = [
`        `"name",
`        `"category",
`        `"slug",
`        `"article",
`        `"description",
`        `"image",
`        `("price", "discount"),
`        `"color",
`        `"consist",
`        `"country",
`    `]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/utils.py**
\# from django.db.models import Q
\#
\# from goods.models import Products
\#
\#
\# def q\_search(query):
\#     if query.isdigit():
\#         return Products.objects.filter(article\_\_exact=int(query))
\#
\#     keywords = [word for word in query.split() if len(word) > 2]
\#
\#     q\_objects = Q()
\#
\#     for token in keywords:
\#         q\_objects |= Q(description\_\_icontains=token)
\#         q\_objects |= Q(name\_\_icontains=token)
\#
\#     return Products.objects.filter(q\_objects)
from django.db.models import Q
from goods.models import Products


def q\_search(query):
`    `# Проверка, если запрос состоит только из цифр
`    `if query.isdigit():
`        `return Products.objects.filter(article\_\_exact=int(query))

`    `q\_objects = Q()

`    `# Поиск по точному вхождению фразы в описании и названии
`    `q\_objects |= Q(description\_\_icontains=query)
`    `q\_objects |= Q(name\_\_icontains=query)

`    `return Products.objects.filter(q\_objects)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/tests.py**
from django.test import TestCase

\# Create your tests here.
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/urls.py**
from django.urls import path
from goods import views

app\_name = 'goods'
urlpatterns = [
`    `path('search/', views.catalog, name='search'),
`    `path('<slug:category\_slug>/', views.catalog, name='index'),
`    `path('product/<slug:product\_slug>/', views.product, name='product'),
]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/views.py**
from django.core.paginator import Paginator
from django.shortcuts import get\_list\_or\_404, get\_object\_or\_404, render

from goods.models import Products, Categories, Sizes, Color, Consist, Country
from goods.utils import q\_search


def catalog(request, category\_slug=None):
`    `page = request.GET.get('page', 1)
`    `on\_sale = request.GET.get('on\_sale', None)
`    `order\_by = request.GET.get('order\_by', None)
`    `query = request.GET.get('q', None)
`    `size\_filters = request.GET.getlist('size')
`    `color\_filters = request.GET.getlist('color')
`    `consist\_filters = request.GET.getlist('consist')
`    `country\_filters = request.GET.getlist('country')

`    `category = ''

`    `if category\_slug == "all":
`        `goods = Products.objects.all()

`    `elif query:
`        `goods = q\_search(query)
`    `else:
`        `goods = Products.objects.filter(category\_\_slug=category\_slug)
`        `category = Categories.objects.get(slug=category\_slug)

`    `if category\_slug == "bryuki":
`        `sizes = Sizes.objects.all().filter(type=2)
`    `elif query:
`        `sizes = Sizes.objects.exclude(name='One size').all()
`    `else:
`        `sizes = Sizes.objects.all().filter(type=1).exclude(name='One size')

`    `if on\_sale:
`        `goods = goods.filter(discount\_\_gt=0)

`    `if size\_filters:
`        `goods = goods.filter(size\_\_id\_\_in=size\_filters).distinct()

`    `if color\_filters:
`        `print(color\_filters)
`        `print(goods.filter(color\_\_id\_\_in=color\_filters))
`        `print(goods.filter(color\_\_id\_\_in=color\_filters).distinct())
`        `goods = goods.filter(color\_\_id\_\_in=color\_filters).distinct()

`    `if consist\_filters:
`        `goods = goods.filter(consist\_\_id\_\_in=consist\_filters).distinct()

`    `if country\_filters:
`        `goods = goods.filter(country\_\_id\_\_in=country\_filters).distinct()

`    `if order\_by and order\_by != "default":
`        `goods = goods.order\_by(order\_by)

`    `goods = goods.filter()
`    `paginator = Paginator(goods, 12)
`    `current\_page = paginator.page(int(page))
`    `page\_query\_param = None



`    `context = {
`        `"title": "Главная - Каталог",
`        `"goods": current\_page,
`        `"slug\_url": category\_slug,
`        `"category\_name": category if category else Categories.objects.get(slug='all'),
`        `'sizes': sizes,
`        `'colors': Color.objects.all(),
`        `'consists': Consist.objects.all(),
`        `'countries': Country.objects.all(),
`        `'selected\_sizes': size\_filters if size\_filters else '',
`        `'selected\_colors': color\_filters if color\_filters else '',
`        `'selected\_consists': consist\_filters if consist\_filters else '',
`        `'selected\_countries': country\_filters if country\_filters else '',
`        `'on\_sale': on\_sale,
`        `'order\_by': order\_by
`    `}
`    `return render(request, "goods/catalog.html", context)


def product(request, product\_slug):
`    `product = Products.objects.get(slug=product\_slug)

`    `context = {"product": product}

`    `return render(request, "goods/product.html", context=context)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/templatetags/\_\_init\_\_.py**

## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/templatetags/goods\_tags.py**
from django import template
from django.utils.http import urlencode
from django.db.models import Case, When, Value, IntegerField, Sum, Q


from goods.models import Categories, Products


register = template.Library()


@register.simple\_tag()
def tag\_categories():
`    `return Categories.objects.annotate(
`        `product\_count=Sum('products\_\_sizeproductrelation\_\_count'),
`        `is\_all=Case(
`            `When(slug='all', then=Value(0)),
`            `default=Value(1),
`            `output\_field=IntegerField()
`        `)
`    `).filter(Q(product\_count\_\_gt=0) | Q(slug='all')).order\_by('is\_all', 'id')


@register.simple\_tag(takes\_context=True)
def change\_params(context, \*\*kwargs):
`    `query = context['request'].GET.dict()
`    `# example with other context vars
`    `# print(context['title'])
`    `# print(context['slug\_url'])
`    `# print(context['goods'])
`    `# print([product.name for product in context['goods']])
`    `query.update(kwargs)
`    `return urlencode(query)


@register.simple\_tag()
def products(slug):
`    `return Products.objects.filter(category\_\_slug=slug)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/templates/goods/product.html**
{% extends "base.html" %}
{% load static %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block content %}
<div class="container mt-5">
`    `<div class="card mb-4 custom-shadow">
`        `<div class="row">
`            `<!-- Миниатюры -->
`            `<div class="col-md-4">
`                `<img src="{{ product.image.url }}"
`                    `class="img-thumbnail" data-bs-toggle="modal" data-bs-target="#imageModal1">
`            `</div>
`            `<div class="col-md-4 ">
`                `<p class="product\_id mt-3">id: {{ product.display\_id }}</p>
`            `</div>
`            `<!-- Увеличить изображение в модальном окне -->
`            `<div class="modal fade" id="imageModal1" tabindex="-1"
`                `aria-labelledby="imageModal1Label" aria-hidden="true">
`                `<div class="modal-dialog modal-lg">
`                    `<div class="modal-content">
`                        `<div class="modal-header">
`                            `<h5 class="modal-title" id="imageModal1Label">{{ product.name }}</h5>
`                            `<button type="button" class="btn-close" data-bs-dismiss="modal"
`                                `aria-label="Закрыть"></button>
`                        `</div>
`                        `<div class="modal-body">
`                            `<img src="{{ product.image.url }}"
`                                `class="img-fluid" alt="Изображение 1">
`                        `</div>
`                    `</div>
`                `</div>
`            `</div>
`        `</div>
`        `<!-- Описание товара -->
`        `<div class="card-body">
`            `<p class="card-text">Цена: <strong>{{ product.sell\_price }} $</strong></p>
`            `<h5 class="card-title">{{ product.name }}</h5>
`            `<p class="card-text">{{ product.description }}</p>
`            `<a href="{% url "cart:cart\_add" %}" class="btn btn-dark add-to-cart"
`            `data-product-id="{{ product.id }}">
`            `{% csrf\_token %}
`            `Добавить в корзину</a>
`        `</div>
`    `</div>
</div>
{% endblock  %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/goods/templates/goods/catalog.html**
{% extends "base.html" %}
{% load static %}
{% load goods\_tags %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block css %}
`    `<style xmlns="http://www.w3.org/1999/html">
.image-container {
`            `position: relative;
`        `}

.button-panel {
`            `position: absolute;
`            `bottom: 0;
`            `width: 100%;
`            `display: flex;
`            `background-color: rgba(29, 77, 81, 0.5);
`            `padding: 5px 0;
`            `opacity: 0;
`            `transition: opacity 0.3s ease;
`        `}

.image-container:hover .button-panel {
`            `opacity: 1;
`        `}

.size {
`            `font-weight: bolder;
`            `color: #e1d89f;;
`        `}

.color-circle {
`            `width: 20px;
`            `height: 20px;
`            `border-radius: 50%;
`            `display: inline-block;
`            `margin-right: 8px;
`        `}
.product::first-letter {
`              `text-transform: uppercase;
`        `}
`    `</style>
{% endblock %}


{% block content %}
<div class="row">
`    `<!-- Форма фильтров -->
`    `<div class="mb-4">
`        `<p style="font-weight: bold; color:  #1d4d51; font-size: 40px; margin-bottom: 0">{% if request.GET.q %} Результаты поиска по запросу {{ request.GET.q }} {% else %}{{ category\_name.name }}{% endif %}</p>
`    `</div>
`    `<div class="dropdown mb-2">
`        `<button class="btn btn-secondary dropdown-toggle btn-dark" type="button" data-bs-toggle="dropdown"
`            `aria-expanded="false" style="background-color: #1d4d51; color: #e1d89f;">
`            `Фильтры
`        `</button>

`        `<form action="{% if request.GET.q %}{% url "catalog:search" %}{% else %}{% url "catalog:index" slug\_url %}{% endif %}" method="get" class="dropdown-menu" style="background-color: #3B575A">
`            `<div class="form-check text-white mx-5">
`                `<input class="form-check-input" type="checkbox" name="on\_sale" id="flexCheckDefault" value="on" {% if request.GET.on\_sale == 'on' %}checked{% endif %} style="cursor: pointer;">
`                `{% if request.GET.q %}
`                    `<input type="hidden" name="q" value="{{ request.GET.q }}">
`                `{% endif %}
`                `<label class="form-check-label" for="flexCheckDefault">
`                    `Товары по акции
`                `</label>
`                `{% if category\_name.filter\_size %}
`                `<p style="margin-left: -50px; margin-top: 10px; margin-bottom: 0">Размер:</p>
`                `{% for size in sizes %}
`                    `<input class="form-check-input" type="checkbox" name="size" id="flexCheckDefault{{ forloop.counter }}" value="{{ size.id }}" {% if size.id|stringformat:"s" in selected\_sizes %}checked{% endif %} style="cursor: pointer;">
`                    `<label class="form-check-label" for="flexCheckDefault{{ forloop.counter }}">
`                        `{{ size.name }}
`                    `</label>
`                    `</br>
`                `{% endfor %}
`                `{% endif %}
`                `<p style="margin-left: -50px; margin-top: 10px; margin-bottom: 0">Цвет:</p>
`                `{% for color in colors %}
`                    `<input class="form-check-input" type="checkbox" name="color" id="flexCheckDefault{{ forloop.counter }}" value="{{ color.id }}" {% if color.id|stringformat:"s" in selected\_colors %}checked{% endif %} style="cursor: pointer;">
`                    `<label class="form-check-label" for="flexCheckDefault{{ forloop.counter }}">
`                        `<span class="color-circle" style="background-color: {{ color.hex }};"></span> {{ color.name }}
`                    `</label>
`                    `</br>
`                `{% endfor %}
`                `{% if category\_name.filter\_consist %}
`                `<p style="margin-left: -50px; margin-top: 10px; margin-bottom: 0">Состав:</p>
`                `{% for consist in consists %}
`                    `<input class="form-check-input" type="checkbox" name="consist" id="flexCheckDefault{{ forloop.counter }}" value="{{ consist.id }}" {% if consist.id|stringformat:"s" in selected\_consists %}checked{% endif %} style="cursor: pointer;">
`                    `<label class="form-check-label" for="flexCheckDefault{{ forloop.counter }}">
`                        `{{ consist.name }}
`                    `</label>
`                    `</br>
`                `{% endfor %}
`                `{% endif %}
`                `<p style="margin-left: -50px; margin-top: 10px; margin-bottom: 0">Страна:</p>
`                `{% for country in countries %}
`                    `<input class="form-check-input" type="checkbox" name="country" id="flexCheckDefault{{ forloop.counter }}" value="{{ country.id }}" {% if country.id|stringformat:"s" in selected\_countries %}checked{% endif %} style="cursor: pointer;">
`                    `<label class="form-check-label" for="flexCheckDefault{{ forloop.counter }}">
`                        `{{ country.name }}
`                    `</label>
`                    `</br>
`                `{% endfor %}
`                `<p class="text-white" style="margin-left: -50px; margin-top: 10px; margin-bottom: 0">Сортировать:</p>
`                `<div class="form-check text-white" style="margin-left: -20px;">
`                    `<input class="form-check-input" type="radio" name="order\_by" id="flexRadioDefault1" value="default"
`                    `{% if not request.GET.order\_by or request.GET.order\_by == 'default' %}checked{% endif %} style="cursor: pointer;">
`                    `<label class="form-check-label" for="flexRadioDefault1">
`                        `По умолчанию
`                    `</label>
`                `</div>
`                `<div class="form-check text-white" style="margin-left: -20px;">
`                    `<input class="form-check-input" type="radio" name="order\_by" id="flexRadioDefault2" value="price"
`                    `{% if request.GET.order\_by == 'price' %}checked{% endif %} style="cursor: pointer;">
`                    `<label class="form-check-label" for="flexRadioDefault2">
`                        `От дешевых к дорогим
`                    `</label>
`                `</div>
`                `<div class="form-check text-white" style="margin-left: -20px;">
`                    `<input class="form-check-input" type="radio" name="order\_by" id="flexRadioDefault3" value="-price"
`                    `{% if request.GET.order\_by == '-price' %}checked{% endif %} style="cursor: pointer;">
`                    `<label class="form-check-label" for="flexRadioDefault3">
`                        `От дорогих к дешевым
`                    `</label>
`                `</div>
`            `</div>
`            `<button type="submit" class="btn mt-3 mb-3" style="margin-left: 170px; background-color: #1d4d51; color: #e1d89f;">Применить</button>
`        `</form>
`    `</div>
`    `{% if not goods %}
`        `<link rel="stylesheet" href="{% static "deps/css/my\_footer\_css.css" %}">
`        `<h2 class="mt-4">По запросу ничего не найдено</h2>
`        `<div style="height: 300px"></div>
`    `{% endif %}
`    `{% for product in goods %}
`        `<!-- Карта товара -->
`        `{% if product.sizeproductrelation\_set.all.total\_count %}
`        `<div class="col-lg-3 col-md-6" style="background-color: #e1d89f;">
`            `<div class="card" style="background-color: #e1d89f; border-color: #e1d89f">
`                `{% if product.image %}
`                    `<div class="image-container">
`                        `<img src="{{ product.image.url }}" class="card-img-top" alt="{{ product.name }}">
`                        `<div class="button-panel">
`                            `{% for sizeproduct in product.sizeproductrelation\_set.all %}
`                                    `{% if sizeproduct.count != 0 %}
`                                        `<a href="{% url "cart:cart\_add" %}" class="btn add-to-cart size" data-product-id="{{ sizeproduct.id }}" data-toggle="tooltip" data-placement="bottom" title="Количество товара: {{ sizeproduct.count }}">
`                                            `{% csrf\_token %} {{ sizeproduct.size.name }}
`                                        `</a>
`                                    `{% endif %}
`                            `{% endfor %}
`                        `</div>
`                        `{% if product.discount %}
`                            `<span class="badge bg-warning text-dark position-absolute top-0 end-0">Скидка {{ product.discount }} %</span>
`                        `{% endif %}
`                    `</div>
`                `{% else %}
`                    `<div class="image-container">
`                        `<img src="{% static "deps/images/Screen Shot 2024-05-27 at 14.54.31.png" %}" class="card-img-top" alt="...">
`                        `<div class="button-panel">
`                            `{% for sizeproduct in product.sizeproductrelation\_set.all %}
`                                    `{% if sizeproduct.count != 0 %}
`                                        `<a href="{% url "cart:cart\_add" %}" class="btn add-to-cart size" data-product-id="{{ sizeproduct.id }}" data-toggle="tooltip" data-placement="bottom" title="Количество товара: {{ sizeproduct.count }}">
`                                            `{% csrf\_token %} {{ sizeproduct.size.name }}
`                                        `</a>
`                                    `{% endif %}
`                            `{% endfor %}
`                        `</div>
`                        `{% if product.discount %}
`                            `<span class="badge bg-warning text-dark position-absolute top-0 end-0">Скидка {{ product.discount }} %</span>
`                        `{% endif %}
`                    `</div>
`                `{% endif %}
`                `<div class="card-body">
`                    `<div class="row">
`                        `<div class="col-7">
`                            `<p class="product" style="font-size: 16px; font-weight: bold; line-height: 15px;">{{ product.name }}</p>
`                        `</div>
`                        `<div class="col-5">
`                            `{% if product.discount %}
`                                `<p style="font-size: 12px; margin-top: -15px; margin-left: -3px"><s>{{product.price}}</s></p>
`                                `<p style="font-size: 16px; font-weight: bold; margin-top: -23px">{{ product.sell\_price }}</p>
`                            `{% else %}
`                            `<p style="font-size: 16px; font-weight: bold">{{ product.price }}</p>
`                            `{% endif %}
`                        `</div>
`                    `</div>
`                    `<p style="font-size: 14px; color: #4d5154; margin-top: -10px">Арт. {{ product.article }}</p>
`                    `<p style="font-size: 14px; color: #4d5154; margin-top: -20px">Цвет: {% for color in product.color.all %} {{ color.name }} {% endfor %}</p>
`                    `{% if product.category.slug != 'aksessuary' %}
`                    `<p style="font-size: 14px; color: #4d5154; margin-top: -20px">Состав: {% for consist in product.consist.all %} {{ consist.name }} {% endfor %}</p>
`                    `{% endif %}
`                    `<p style="font-size: 14px; color: #4d5154; margin-top: -20px">Страна: {{ product.country.name }}</p>
`                `</div>
`            `</div>
`        `</div>
`        `{% endif %}
`    `{% endfor %}



</div>
<!-- Пагинация -->
{% if goods %}
`    `<nav aria-label="Page navigation example">
`        `<ul class="pagination justify-content-center my-4">
`            `<div class="custom-shadow d-flex">

`                `<li class="page-item {% if not goods.has\_previous %}disabled{% endif %}">
`                `<a class="page-link" href="{% if goods.has\_previous %}?{% change\_params page=goods.previous\_page\_number %}{% else %}#{% endif %}">Назад</a>
`                `</li>

`                `{% for page in goods.paginator.page\_range %}
`                `{% if page >= goods.number|add:-2 and page <= goods.number|add:2 %}
`                    `<li class="page-item {% if goods.number == page %} active {% endif %}">
`                        `<a class="page-link" href="?{% change\_params page=page %}">{{ page }}</a>
`                    `</li>
`                `{% endif %}
`                `{% endfor %}


`                `<li class="page-item {% if not goods.has\_next %}disabled{% endif %}">
`                    `<a class="page-link" href="{% if goods.has\_next %}?{% change\_params page=goods.next\_page\_number %}{% else %}#{% endif %}">Следующая</a>
`                `</li>
`            `</div>
`        `</ul>
`    `</nav>
{% endif %}
{% endblock  %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/signals.py**
from django.db.models.signals import post\_save
from django.dispatch import receiver
from django.core.mail import send\_mail
from django.conf import settings
from .models import Order
\# from auditlog.registry import auditlog

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

\# auditlog.register(Order)


fromaddr = 'demenkovakatarina@mail.ru'
mypass = "93XqCqhdZgaTje3KUut0"


def send(msg: MIMEMultipart, toaddr: str):
`    `server = smtplib.SMTP\_SSL('smtp.mail.ru', 465)
`    `server.login(fromaddr, mypass)
`    `text = msg.as\_string()
`    `server.sendmail(fromaddr, toaddr, text)
`    `server.quit()


STATUS\_CHOICES = [
`    `{'id': 'processing', 'name': 'В обработке'},
`    `{'id': 'ready', 'name': 'Готов к выдаче'},
`    `{'id': 'completed', 'name': 'Завершен'},
`    `{'id': 'cancelled', 'name': 'Отменен'},
]


@receiver(post\_save, sender=Order)
def send\_email\_on\_field\_change(sender, instance, created, \*\*kwargs):

`    `if not created:
`        `# print(Order.objects.get(pk=instance.pk).status)

`        `msg = MIMEMultipart()
`        `msg['From'] = fromaddr
`        `msg['To'] = instance.email
`        `msg['Subject'] = f"Обновление статуса заказа №{instance.pk}"


`        `status = ''
`        `for st in STATUS\_CHOICES:
`            `if st['id'] == instance.status:
`                `status = st['name']
`        `if instance.status == 'ready':
`            `sum = 0
`            `for item in Order.objects.get(pk=instance.pk).orderitem\_set.all():
`                `print(Order.objects.get(pk=instance.pk).orderitem\_set.all())
`                `sum += item.price

`            `body = f"<h4>Статус заказа: {status}.</h4><h5>К оплате: <strong>{sum}</strong></h5><h5>Адрес: ул. Улица Октябрьской Революции, 23, город Смоленск</h5>"
`        `else:
`            `body = f"<h4>Статус заказа: {status}.</h4>"
`        `msg.attach(MIMEText(body, 'html'))

`        `send(msg, instance.email)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/order.vue**
<template>
`  `<div class="about-page mt-3">
`    `<h2 class="m-2" style="color: #1d4d51; margin-bottom: 40px!important;"><strong>О нас</strong></h2>
`    `<div class="info-block">
`      `<p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
`        `<img class="mx-1" src="/deps/icons/time-br.svg"
`             `alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Режим работы:
`      `</p>
`      `<p style="margin-left: 250px; font-size: 16px; margin-bottom: 0; margin-top: -45px">
`        `пн-пт <strong>10:00 - 19:00</strong>
`      `</p>
`      `<p style="margin-left: 250px; font-size: 16px; margin-top: 0">
`        `сб-вс <strong>10:00 - 17:00</strong>
`      `</p>
`    `</div>
`    `<div class="info-block">
`      `<p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
`        `<img class="mx-1" src="/deps/icons/phone-br.svg"
`             `alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Телефон:
`        `<span style="margin-left: 70px; font-size: 16px; margin-bottom: 0">+7 (950) 700-66-48</span>
`      `</p>
`    `</div>
`    `<div class="info-block">
`      `<p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
`        `<img class="mx-1" src="/deps/icons/mail-br.svg"
`             `alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Mail:
`        `<span style="margin-left: 110px; font-size: 16px; margin-bottom: 0">passag@mail.ru</span>
`      `</p>
`    `</div>
`    `<div class="info-block">
`      `<p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
`        `<img class="mx-1" src="/deps/icons/adres-br.svg"
`             `alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Адрес:
`        `<span style="margin-left: 90px; font-size: 16px; margin-bottom: 0">ул. Улица Октябрьской Революции, 23, город Смоленск</span>
`      `</p>
`    `</div>
`    `<iframe src="https://yandex.com/map-widget/v1/?um=constructor%3Aec8f4363eaa5434b6052a4e24b1f8aacc07b98c982486aa1e07b67ca74afc9e3&amp;source=constructor"
`            `width="400" height="300" style="margin-left: 250px"></iframe>
`  `</div>
</template>

<script>
export default {
`  `name: 'About'
}
</script>

<style scoped>
.about-page {
`  `margin-top: 3rem;
}
.info-block {
`  `margin-bottom: 10px;
}
.mx-1 {
`  `margin-left: 0.25rem;
`  `margin-right: 0.25rem;
}
</style>
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/models.py**
from django.db import models
from goods.models import Products, SizeProductRelation

from users.models import User


class OrderitemQueryset(models.QuerySet):

`    `def total\_price(self):
`        `return sum(cart.products\_price() for cart in self)

`    `def total\_quantity(self):
`        `if self:
`            `return sum(cart.quantity for cart in self)
`        `return 0


class Order(models.Model):
`    `PROCESSING = 'processing'
`    `READY = 'ready'
`    `COMPLETED = 'completed'
`    `CANCELLED = 'cancelled'

`    `STATUS\_CHOICES = [
`        `(PROCESSING, 'В обработке'),
`        `(READY, 'Готов к выдаче'),
`        `(COMPLETED, 'Завершен'),
`        `(CANCELLED, 'Отменен'),
`    `]

`    `user = models.ForeignKey(to=User, on\_delete=models.SET\_DEFAULT, blank=True, null=True, verbose\_name="Пользователь",
`                             `default=None)
`    `created\_timestamp = models.DateTimeField(auto\_now\_add=True, verbose\_name="Дата создания заказа")
`    `phone\_number = models.CharField(max\_length=20, verbose\_name="Номер телефона")
`    `email = models.EmailField(verbose\_name="Электронная почта", max\_length=254)
`    `# requires\_delivery = models.BooleanField(default=False, verbose\_name="Требуется доставка")
`    `# delivery\_address = models.TextField(null=True, blank=True, verbose\_name="Адрес доставки")
`    `# payment\_on\_get = models.BooleanField(default=False, verbose\_name="Оплата при получении")
`    `# is\_paid = models.BooleanField(default=False, verbose\_name="Оплачено")
`    `status = models.CharField(max\_length=50, choices=STATUS\_CHOICES, default=PROCESSING, verbose\_name="Статус заказа")

`    `class Meta:
`        `db\_table = "order"
`        `verbose\_name = "Заказ"
`        `verbose\_name\_plural = "Заказы"

`    `def \_\_str\_\_(self):
`        `return f"Заказ № {self.pk} | Покупатель {self.user.first\_name} {self.user.last\_name}"


class OrderItem(models.Model):
`    `order = models.ForeignKey(to=Order, on\_delete=models.CASCADE, verbose\_name="Заказ")
`    `sizeproduct = models.ForeignKey(to=SizeProductRelation, on\_delete=models.SET\_DEFAULT, null=True, verbose\_name="Продукт",
`                                `default=None)
`    `name = models.CharField(max\_length=150, verbose\_name="Название")
`    `price = models.DecimalField(max\_digits=7, decimal\_places=2, verbose\_name="Цена")
`    `quantity = models.PositiveIntegerField(default=0, verbose\_name="Количество")
`    `created\_timestamp = models.DateTimeField(auto\_now\_add=True, verbose\_name="Дата продажи")

`    `class Meta:
`        `db\_table = "order\_item"
`        `verbose\_name = "Проданный товар"
`        `verbose\_name\_plural = "Проданные товары"

`    `objects = OrderitemQueryset.as\_manager()

`    `def products\_price(self):
`        `return round(self.sizeproduct.product.sell\_price() \* self.quantity, 2)

`    `def \_\_str\_\_(self):
`        `return f"Товар {self.name} | Заказ № {self.order.pk}"
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/\_\_init\_\_.py**

## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/apps.py**
from django.apps import AppConfig


class OrdersConfig(AppConfig):
`    `default\_auto\_field = 'django.db.models.BigAutoField'
`    `name = 'orders'
`    `verbose\_name='Заказы'

`    `def ready(self):
`        `import orders.signals
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/forms.py**
import re
from django import forms


class CreateOrderForm(forms.Form):
`    `# first\_name = forms.CharField()
`    `# last\_name = forms.CharField()
`    `phone\_number = forms.CharField()
`    `email = forms.EmailField()
`    `# requires\_delivery = forms.ChoiceField(
`    `#     choices=[
`    `#         ("0", False),
`    `#         ("1", True),
`    `#     ],
`    `# )
`    `# delivery\_address = forms.CharField(required=False)
`    `# payment\_on\_get = forms.ChoiceField(
`    `#     choices=[
`    `#         ("0", 'False'),
`    `#         ("1", 'True'),
`    `#     ],
`    `# )

`    `def clean\_phone\_number(self):
`        `data = self.cleaned\_data['phone\_number']

`        `if not data.isdigit():
`            `raise forms.ValidationError("Номер телефона должен содержать только цифры")

`        `pattern = re.compile(r'^\d{10}$')
`        `if not pattern.match(data):
`            `raise forms.ValidationError("Неверный формат номера")

`        `return data

`    `# first\_name = forms.CharField(
`    `#     widget=forms.TextInput(
`    `#         attrs={
`    `#             "class": "form-control",
`    `#             "placeholder": "Введите ваше имя",
`    `#         }
`    `#     )
`    `# )

`    `# last\_name = forms.CharField(
`    `#     widget=forms.TextInput(
`    `#         attrs={
`    `#             "class": "form-control",
`    `#             "placeholder": "Введите вашу фамилию",
`    `#         }
`    `#     )
`    `# )

`    `# phone\_number = forms.CharField(
`    `#     widget=forms.TextInput(
`    `#         attrs={
`    `#             "class": "form-control",
`    `#             "placeholder": "Номер телефона",
`    `#         }
`    `#     )
`    `# )

`    `# requires\_delivery = forms.ChoiceField(
`    `#     widget=forms.RadioSelect(),
`    `#     choices=[
`    `#         ("0", False),
`    `#         ("1", True),
`    `#     ],
`    `#     initial=0,
`    `# )

`    `# delivery\_address = forms.CharField(
`    `#     widget=forms.Textarea(
`    `#         attrs={
`    `#             "class": "form-control",
`    `#             "id": "delivery-address",
`    `#             "rows": 2,
`    `#             "placeholder": "Введите адрес доставки",
`    `#         }
`    `#     ),
`    `#     required=False,
`    `# )

`    `# payment\_on\_get = forms.ChoiceField(
`    `#     widget=forms.RadioSelect(),
`    `#     choices=[
`    `#         ("0", 'False'),
`    `#         ("1", 'True'),
`    `#     ],
`    `#     initial="card",
`    `# )
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/admin.py**
from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemTabulareAdmin(admin.TabularInline):
`    `model = OrderItem
`    `fields = "sizeproduct", "name", "price", "quantity"
`    `search\_fields = (
`        `"sizeproduct",
`        `"name",
`    `)
`    `extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
`    `list\_display = "order", "sizeproduct", "name", "price", "quantity"
`    `search\_fields = (
`        `"order",
`        `"sizeproduct",
`        `"name",
`    `)


class OrderTabulareAdmin(admin.TabularInline):
`    `model = Order
`    `fields = (
`        `"status",
`        `"created\_timestamp",
`    `)

`    `search\_fields = (
`        `"created\_timestamp",
`    `)
`    `readonly\_fields = ("created\_timestamp",)
`    `extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
`    `list\_display = (
`        `"id",
`        `"user",
`        `"status",
`        `"created\_timestamp",
`    `)

`    `search\_fields = (
`        `"id",
`    `)
`    `readonly\_fields = ("created\_timestamp", "id", "user", "email", "phone\_number")
`    `list\_filter = (
`        `"status",
`    `)
`    `inlines = (OrderItemTabulareAdmin,)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/tests.py**
from django.test import TestCase

\# Create your tests here.
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/urls.py**
from django.urls import path

from orders import views

app\_name = 'orders'

urlpatterns = [
`    `path('create-order/', views.create\_order, name='create\_order'),
]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/views.py**
from django.contrib import messages
from django.contrib.auth.decorators import login\_required
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from carts.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from users.models import User


@login\_required
def create\_order(request):
`    `if request.method == 'POST':
`        `form = CreateOrderForm(data=request.POST)
`        `if form.is\_valid():
`            `try:
`                `with transaction.atomic():
`                    `user = request.user
`                    `cart\_items = Cart.objects.filter(user=user)

`                    `if cart\_items.exists():
`                        `# Создать заказ
`                        `order = Order.objects.create(
`                            `user=user,
`                            `phone\_number=form.cleaned\_data['phone\_number'],
`                            `email=form.cleaned\_data['email']
`                        `)
`                        `# Создать заказанные товары
`                        `for cart\_item in cart\_items:
`                            `sizeproduct = cart\_item.sizeproduct
`                            `name = cart\_item.sizeproduct.product.name
`                            `price = cart\_item.sizeproduct.product.sell\_price()
`                            `quantity = cart\_item.quantity

`                            `if sizeproduct.count < quantity:
`                                `raise ValidationError(f'Недостаточное количество товара {name} на складе\
`                                                       `В наличии - {sizeproduct.count}')

`                            `OrderItem.objects.create(
`                                `order=order,
`                                `sizeproduct=sizeproduct,
`                                `name=name,
`                                `price=price,
`                                `quantity=quantity,
`                            `)
`                            `sizeproduct.count -= quantity
`                            `sizeproduct.save()

`                        `# Очистить корзину пользователя после создания заказа
`                        `cart\_items.delete()

`                        `messages.success(request, 'Заказ оформлен!')
`                        `return redirect('user:profile')
`            `except ValidationError as e:
`                `messages.success(request, str(e))
`                `return redirect('cart:order')
`    `else:
`        `print(request.user)
`        `initial = {
`            `'first\_name': request.user.first\_name,
`            `'last\_name': request.user.last\_name,
`            `'phone\_number': User.objects.get(username=request.user.username).phone\_number,
`            `'email': request.user.email,
`        `}

`        `form = CreateOrderForm(initial=initial)

`    `context = {
`        `'title': 'Home - Оформление заказа',
`        `'form': form,
`        `'order': True,
`    `}
`    `return render(request, 'orders/create\_order.html', context=context)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/orders/templates/orders/create\_order.html**
{% extends "base.html" %}
{% load static %}
{% load carts\_tags %}

{% block content %}
<div class=" bg-white p-4 mb-4 mx-2 rounded custom-shadow">
`    `<div class="container">
`        `<h3 class="text-center mb-4">Выбранные товары</h3>
`        `<div class="container" id="cart-items-container">
`            `<!-- Разметка корзины -->
`            `{% user\_carts request as carts %}

{#            {% include "carts/includes/included\_cart.html" %}#}
`            `{% for cart in carts %}
`                `<ul class="list-group">
`                    `<li class="list-group-item" style="border-color: #ffffff">
`                        `<div class="row">
`                            `<div class="col-1">
`                                `<img src="{{ cart.sizeproduct.product.image.url }}" alt="..." height="90px" width="65px">
`                            `</div>
`                            `<div class="col-6" style="padding-left: 30px">
`                                `<h5 class="card-title mb-1">{{ cart.sizeproduct.product.name }}</h5>
`                                `<p style="margin-top:0; margin-bottom: 0; font-size: 15px">Размер: {{ cart.sizeproduct.size.name }}</p>
`                                `<p style="margin-top:0; margin-bottom: 0">Цвет: {% for color in cart.sizeproduct.product.color.all %} {{ color.name }} {% endfor %}</p>
`                                `<p class="mt-0">Состав: {% for consist in cart.sizeproduct.product.consist.all %} {{ consist.name }} {% endfor %}</p>
`                            `</div>
`                            `<div class="col-4">
`                                `<h5>{{cart.products\_price}} Р</h5>
`                                `<div class="btn-group btn-group-sm mt-2 input-group" role="group" aria-label="First group" style="max-width: 90px">
`                                    `<button type="button" class="btn btn-outline-secondary decrement" data-cart-id="{{ cart.id }}" data-cart-change-url="{% url 'cart:cart\_change' %}" style="width: 25px">
`                                        `{% csrf\_token %}
`                                        `-</button>
`                                    `<input type="text" class="form-control number" value="{{ cart.quantity }}" style="border-color: #4d5154; border-radius: 0; max-width: 25px; padding: 1px 8px 1px 5px;" readonly>
`                                    `{% if cart.quantity < cart.sizeproduct.count %}
`                                    `<button type="button" class="btn btn-outline-secondary increment" data-cart-id="{{ cart.id }}" data-cart-change-url="{% url 'cart:cart\_change' %}" style="width: 25px">
`                                        `{% csrf\_token %}
`                                        `+</button>
`                                    `{% else %}
`                                    `<button type="button" class="btn btn-outline-secondary" style="width: 25px" disabled>
`                                        `+</button>
`                                    `{% endif %}
`                                `</div>
`                                `<a href="{% url "cart:cart\_remove" %}" class="remove-from-cart"
`                                   `data-cart-id="{{ cart.id }}" style="margin-left: 40px" data-toggle="tooltip" data-placement="bottom" title="Удалить">
`                                    `{% csrf\_token %}
`                                    `<img class="mx-1" src="{% static "deps/icons/trash-red.svg" %}"
`                                        `alt="Catalog Icon" width="20" height="20">
`                                `</a>
`                            `</div>
`                        `</div>
`                    `</li>
`                    `<hr class="mt-0 mb-1">
`                `</ul>
`        `{% endfor %}
`        `<div class="row">
`            `<h4 class="col-7 float-left"><strong>Итого</strong></h4>
`            `<h4 class="col-5"><strong>{{ carts.total\_price }} Р</strong></h4>
`        `</div>
`            `<!-- Закончилась разметка корзины -->
`        `</div>
`    `</div>
`    `<!-- Детали заказа -->
`    `<div class="container mt-3">
`        `<h3 class="text-center mb-3">Контакты получателя</h3>
`        `<div class="card mb-3">
`            `<div class="card-body">
`                `<form action="{% url "orders:create\_order" %}" method="post" id="orderForm" novalidate>
`                    `{% csrf\_token %}
`                    `{{ form.non\_field\_errors }}
`                    `<div class="row">
`                        `<div class="col-md-6 mb-3">
`                            `<div class="form-group">
`                                `<label for="id\_phone\_number" class="form-label">Номер телефона\*:</label>
`                                `<input type="text" class="form-control" id="id\_phone\_number" name="phone\_number"
`                                    `value="{% if form.phone\_number.value %}{{ form.phone\_number.value }}{% endif %}"
`                                    `placeholder="В формате: XXX-XXX-XX-XX"
`                                    `required>
`                            `{% if form.phone\_number.errors %}
`                                `<div class="errors" style="color: red; margin-top: 5px;">{{form.phone\_number.errors}}</div>
`                            `{% endif %}
`                            `</div>
`                        `</div>
`                        `<div class="col-md-6 mb-3">
`                            `<div class="form-group">
`                                `<label for="id\_email" class="form-label">Email\*:</label>
`                                `<input type="email" class="form-control" id="id\_email" name="email"
`                                    `value="{% if form.email.value %}{{ form.email.value }}{% endif %}"
`                                    `required>
`                            `{% if form.email.errors %}
`                                `<div class="errors" style="color: red; margin-top: 5px;">{{form.email.errors}}</div>
`                            `{% endif %}
`                            `</div>
`                        `</div>
`                    `</div>
`                    `<div class="row">
`                        `<div class="col-9">
`                        `</div>
`                        `<div class="col-3">
`                            `<button type="submit" class="btn btn-dark" style="background-color: #1d4d51; color: #e1d89f">Оформить заказ</button>
`                        `</div>
`                    `</div>
`                `</form>
`            `</div>
`        `</div>
`    `</div>
</div>

{#    <script>#}
{#        $(document).ready(function() {#}
{#            $('#orderForm').on('submit', function(event) {#}
{#                let valid = true;#}
{#                let phone\_number = $('#id\_phone\_number');#}
{#                let phone\_numberError = $('#phone\_numberError');#}
{#                let email = $('#id\_email');#}
{#                let emailError = $('#emailError');#}
{##}
{#                if (phone\_number.val() === '') {#}
{#                    valid = false;#}
{#                    phone\_numberError.text('Пожалуйста, введите номер телефона.');#}
{#                } else {#}
{#                    phone\_numberError.text('');#}
{#                }#}
{##}
{#                if (!valid) {#}
{#                    event.preventDefault();#}
{#                }#}
{#            });#}
{#        });#}
{#    </script>#}
{% endblock  %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/models.py**
from django.db import models

\# Create your models here.
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/\_\_init\_\_.py**

## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/apps.py**
from django.apps import AppConfig


class MainConfig(AppConfig):
`    `default\_auto\_field = 'django.db.models.BigAutoField'
`    `name = 'main'
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/forms.py**
from django import forms
from goods.models import Categories
from django.db.models import Q, Sum


class ExportForm(forms.Form):

`    `category = forms.ModelChoiceField(queryset=Categories.objects.annotate(product\_count=Sum('products\_\_sizeproductrelation\_\_count')).filter(Q(product\_count\_\_gt=0)), required=True)
`    `start\_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
`    `end\_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/admin.py**
from django.contrib import admin

\# Register your models here.
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/tests.py**
from django.test import TestCase

\# Create your tests here.
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/urls.py**

from django.urls import path
from main import views

app\_name = 'main'
urlpatterns = [
`    `path('', views.index, name='index'),
`    `path('about/', views.about, name='about'),
`    `path('panel/', views.panel, name='panel'),
]
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/views.py**
from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Products
from main.forms import ExportForm
import os
from openpyxl import Workbook
from openpyxl.styles import Border, Side, Alignment, Font, PatternFill, NamedStyle
from openpyxl.styles.colors import COLOR\_INDEX
from typing import List, Dict, Union
from datetime import datetime
from urllib.parse import quote


\# Create your views here.
def index(request):

`    `context = {
`        `'title': 'Главная',
`        `'content': 'Магазин женской одежды - Пассаж',
`    `}
`    `return render(request, 'main/index.html', context)


def about(request):
`    `context = {
`        `'title': 'Главная - О нас',
`        `'content': 'О нас',
`    `}
`    `return render(request, 'main/about.html', context)


def panel(request):
`    `if request.method == 'POST':
`        `form = ExportForm(request.POST)
`        `if form.is\_valid():
`            `category\_name = form.cleaned\_data['category']
`            `start\_date = form.cleaned\_data['start\_date']
`            `end\_date = form.cleaned\_data['end\_date']

`            `products = Products.objects.filter(category\_\_name=category\_name)

`            `if start\_date:
`                `products = products.filter(created\_at\_\_gte=start\_date)
`            `if end\_date:
`                `products = products.filter(created\_at\_\_lte=end\_date)

`            `wb: Workbook = Workbook()
`            `ws = wb.active
`            `ws.title = f'Товары'

`            `headers: List[Dict[str, Union[str, int]]] = [
`                `{'name': 'code', 'title': 'Код товара', 'width': 20, 'stroka2': 'GTIN', 'stroka3': 'value', 'stroka4': ''},
`                `{'name': 'tnvd', 'title': 'Код ТНВЭД', 'width': 20, 'stroka2': 'Tnved', 'stroka3': 'value', 'stroka4': ''},
`                `{'name': 'name', 'title': 'Полное наименование товара', 'width': 40, 'stroka2': '2478', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'znak', 'title': 'Товарный знак', 'width': 30, 'stroka2': '2504', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'article', 'title': 'Артикул производителя', 'width': 30, 'stroka2': '13914', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'category', 'title': 'Вид товара', 'width': 20, 'stroka2': '12', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'color', 'title': 'Цвет', 'width': 20, 'stroka2': '36', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'pol', 'title': 'Целевой пол', 'width': 20, 'stroka2': '14013', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'size', 'title': 'Размер одежды изделия', 'width': 20, 'stroka2': '35', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'consist', 'title': 'Состав', 'width': 20, 'stroka2': '2483', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'codetnvd', 'title': 'Код ТНВЭД', 'width': 20, 'stroka2': '13933', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'reglament', 'title': 'Номер технического регламента', 'width': 60, 'stroka2': '13836', 'stroka3': 'value', 'stroka4': 'Текстовое значение'},
`                `{'name': 'status', 'title': 'Статус карточки товара в Каталоге', 'width': 40, 'stroka2': 'status', 'stroka3': 'value', 'stroka4': 'Текстовое поле(Черновик или На модерации)'},
`                `{'name': 'result', 'title': 'Результат обработки данных в Каталоге', 'width': 40, 'stroka2': 'result', 'stroka3': 'value', 'stroka4': 'Заполняется автоматически при загрузке в систему'}
`            `]

`            `table\_style = NamedStyle(name='table\_style')
`            `table\_style.font = Font(name='Arial')

`            `for position, header in enumerate(headers):
`                `ws.cell(1, position + 1, header['title']).alignment = Alignment(horizontal="center", vertical="center", wrap\_text=True)
`                `ws.cell(1, position + 1, header['title']).font = Font(name='Arial', bold=True)
`                `ws.cell(1, position + 1, header['title']).fill = PatternFill(fgColor=COLOR\_INDEX[5], fill\_type="solid")
`                `ws.cell(1, position + 1, header['title']).border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

`                `ws.cell(2, position + 1, header['stroka2']).alignment = Alignment(horizontal="center", vertical="center", wrap\_text=True)
`                `ws.cell(2, position + 1, header['stroka2']).font = Font(name='Arial')
`                `ws.cell(2, position + 1, header['stroka2']).fill = PatternFill(fgColor='E3E1E4', fill\_type="solid")
`                `ws.cell(2, position + 1, header['stroka2']).border = Border(left=Side(style='thin'),
`                                                                          `right=Side(style='thin'),
`                                                                          `top=Side(style='thin'),
`                                                                          `bottom=Side(style='thin'))

`                `ws.cell(3, position + 1, header['stroka3']).alignment = Alignment(horizontal="center", vertical="center", wrap\_text=True)
`                `ws.cell(3, position + 1, header['stroka3']).font = Font(name='Arial')
`                `ws.cell(3, position + 1, header['stroka3']).fill = PatternFill(fgColor='E3E1E4', fill\_type="solid")
`                `ws.cell(3, position + 1, header['stroka3']).border = Border(left=Side(style='thin'),
`                                                                          `right=Side(style='thin'),
`                                                                          `top=Side(style='thin'),
`                                                                          `bottom=Side(style='thin'))

`                `ws.cell(4, position + 1, header['stroka4']).alignment = Alignment(horizontal="center", vertical="center", wrap\_text=True)
`                `ws.cell(4, position + 1, header['stroka4']).font = Font(name='Arial')
`                `ws.cell(4, position + 1, header['stroka4']).fill = PatternFill(fgColor='E3E1E4', fill\_type="solid")
`                `ws.cell(4, position + 1, header['stroka4']).border = Border(left=Side(style='thin'),
`                                                                          `right=Side(style='thin'),
`                                                                          `top=Side(style='thin'),
`                                                                          `bottom=Side(style='thin'))

`                `ws.column\_dimensions[ws.cell(1, position + 1).column\_letter].width = header['width']

`                `start\_position: int = 5
`                `for product in products:
`                    `for sizeproduct in product.sizeproductrelation\_set.all():
`                        `if sizeproduct.count > 0:
`                            `for position, header in enumerate(headers):
`                                `if header['name'] == 'tnvd':
`                                    `ws.cell(start\_position, position + 1).value = sizeproduct.product.category.tnved
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'name':
`                                    `ws.cell(start\_position,
`                                            `position + 1).value = f'{sizeproduct.product.name}, р.{sizeproduct.size.name}, арт.{sizeproduct.product.article}'
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'znak':
`                                    `ws.cell(start\_position, position + 1).value = 'Без товарного знака'
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'article':
`                                    `ws.cell(start\_position, position + 1).value = sizeproduct.product.article
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'category':
`                                    `ws.cell(start\_position, position + 1).value = sizeproduct.product.category.name
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'color':
`                                    `colors\_names = [color.name for color in sizeproduct.product.color.all()]
`                                    `colors\_string = ", ".join(colors\_names)
`                                    `ws.cell(start\_position, position + 1).value = colors\_string
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'pol':
`                                    `ws.cell(start\_position, position + 1).value = 'ЖЕНСКИЙ'
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'size':
`                                    `ws.cell(start\_position, position + 1).value = sizeproduct.size.name
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'consist':
`                                    `consists\_names = [consist.name for consist in sizeproduct.product.consist.all()]
`                                    `consists\_string = ", ".join(consists\_names)
`                                    `ws.cell(start\_position, position + 1).value = consists\_string
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'codetnvd':
`                                    `ws.cell(start\_position, position + 1).value = f'{sizeproduct.product.category.tnved}000000'
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'reglament':
`                                    `ws.cell(start\_position, position + 1).value = 'TP TC 017/2011 "О безопасности продукции легкой промышленности"'
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                                `elif header['name'] == 'status':
`                                    `ws.cell(start\_position, position + 1).value = 'Черновик'
`                                    `ws.cell(start\_position, position + 1).style = table\_style
`                            `start\_position += 1

`            `filename = f'products\_{category\_name}\_{datetime.now().strftime("%d-%m-%Y\_%H-%M-%S")}.xlsx'
`            `filepath = os.path.join('media', filename)
`            `wb.save(filepath)

`            `with open(filepath, 'rb') as f:
`                `response = HttpResponse(f.read(),
`                                        `content\_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
`                `response['Content-Disposition'] = 'attachment; filename="{}"'.format(quote(filename))

`            `return response

`    `else:
`        `form = ExportForm()

`    `context = {
`        `'title': 'Главная - Панель администратора',
`        `'content': 'Панель администратора',
`        `'form': form
`    `}
`    `return render(request, 'main/panel.html', context)
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/templates/main/index.html**
{% extends "base.html" %}
{% load static %}
{% load goods\_tags %}

{% block css %}
`    `<link rel="stylesheet" href="{% static "deps/css/my\_footer\_css.css" %}">
{% endblock %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block content %}
`    `<h1 style="color: #1d4d51;"><strong>Магазин женской одежды</strong></h1>
`    `<div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel" style="margin-top: 40px; margin-bottom: 20px">
`      `<div class="carousel-inner">
`        `<div class="carousel-item active" style="margin-left: 90px">
`          `<img src="/static/deps/images/Screen%20Shot%202024-05-26%20at%2018.43.36.png" class="d-block w-75" alt="...">
`        `</div>
`        `<div class="carousel-item" style="margin-left: 90px">
`          `<img src="/static/deps/images/ZkNExs5xTBE.jpeg" class="d-block w-75" alt="...">
`        `</div>
`      `</div>
`      `<button style="margin-left: 20px" class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
`        `<span class="carousel-control-prev-icon" aria-hidden="true"></span>
`        `<span class="visually-hidden">Previous</span>
`      `</button>
`      `<button style="margin-right: 115px" class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
`        `<span class="carousel-control-next-icon" aria-hidden="true"></span>
`        `<span class="visually-hidden">Next</span>
`      `</button>
`    `</div>
{% endblock %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/templates/main/about.html**
{% extends "base.html" %}
{% load static %}

{% block css %}
`    `<link rel="stylesheet" href="{% static "deps/css/my\_footer\_css.css" %}">
{% endblock %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block content %}
`    `<div class="mt-3">
`        `<h2 class="m-2" style="color: #1d4d51; margin-bottom: 40px!important;"><strong>О нас</strong></h2>
`        `<p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
`            `<img class="mx-1" src="{% static "deps/icons/time-br.svg" %}"
`                                `alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Режим работы:
`            `<p style="margin-left: 250px; font-size: 16px; margin-bottom: 0; margin-top: -45px">пн-пт <strong>10:00 - 19:00</strong></p>
`            `<p style="margin-left: 250px; font-size: 16px; margin-top: 0">сб-вс <strong>10:00 - 17:00</strong></p>
`        `</p>
`        `<p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
`            `<img class="mx-1" src="{% static "deps/icons/phone-br.svg" %}"
`                 `alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Телефон: <span style="margin-left: 70px; font-size: 16px; margin-bottom: 0">+7 (950) 700-66-48</span>
`        `</p>
`        `<p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
`            `<img class="mx-1" src="{% static "deps/icons/mail-br.svg" %}"
`                 `alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Mail: <span style="margin-left: 110px; font-size: 16px; margin-bottom: 0">passag@mail.ru</span>
`        `</p>
`        `<p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
`            `<img class="mx-1" src="{% static "deps/icons/adres-br.svg" %}"
`                 `alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Адрес: <span style="margin-left: 90px; font-size: 16px; margin-bottom: 0">ул. Улица Октябрьской Революции, 23, город Смоленск</span>
`        `</p>
`        `<iframe src="https://yandex.com/map-widget/v1/?um=constructor%3Aec8f4363eaa5434b6052a4e24b1f8aacc07b98c982486aa1e07b67ca74afc9e3&amp;source=constructor" width="400" height="300" style="margin-left: 250px"></iframe>
`    `</div>
{% endblock %}
## **Файл: /Users/katedem/PycharmProjects/shop-passag/main/templates/main/panel.html**
{#{% extends "base.html" %}#}
{#{% load static %}#}
{##}
{#{% block css %}#}
{#    <link rel="stylesheet" href="{% static "deps/css/my\_footer\_css.css" %}">#}
{#    <style>#}
{#        .error {#}
{#            color: red;#}
{#            margin-top: 5px;#}
{#        }#}
{#    </style>#}
{#    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">#}
{#    <!-- Подключаем jQuery UI CSS -->#}
{#    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.css">#}
{#{% endblock %}#}
{##}
{#{% block modal\_cart %}#}
{#{% include "includes/cart\_button.html" %}#}
{#{% endblock  %}#}
{##}
{#{% block content %}#}
{#    <div class="mt-3">#}
{#        <h2 class="m-2" style="color: #1d4d51"><strong>{{ content }}</strong></h2>#}
{#        <div class="row mt-5" style="margin-left: 20px">#}
{#            <a class="icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.125rem, 0); color: #1d4d51; text-decoration-color: #1d4d51" href="{% url "admin:index" %}">#}
{#              <img class="bi" src="{% static "deps/icons/profile-br.svg" %}" alt="Catalog Icon" style="width: 40px; height: 40px; margin-bottom: 7px">#}
{#                <h3>Администрирование сайта</h3>#}
{#            </a>#}
{#        </div>#}
{#        <div class="row mt-4" style="margin-left: 20px">#}
{#            <a id="modalButton2" type="button" class="icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.125rem, 0); color: #1d4d51; text-decoration-color: #1d4d51">#}
{#              <img class="bi" src="{% static "deps/icons/excel.svg" %}" alt="Catalog Icon" style="width: 40px; height: 40px; margin-bottom: 7px">#}
{#                <h3>Выгрузить товары</h3>#}
{#            </a>#}
{#        </div>#}
{#        <div class="modal fade" id="exampleModal2" tabindex="-1" aria-labelledby="exampleModalLabel"#}
{#            aria-hidden="true">#}
{#            <div class="modal-dialog modal-dialog-scrollable">#}
{#                <div class="modal-content" style="">#}
{#                    <div class="modal-header" style="border: none; margin-top: 10px; margin-right: 10px">#}
{#                        <button type="button" class="btn-close" data-bs-dismiss="modal"#}
{#                            aria-label="Close"></button>#}
{#                    </div>#}
{#                    <div class="modal-body">#}
{#                        <h3 class="text-center mb-4" style="color: #1d4d51; margin-top: -20px">Выгрузка товаров</h3>#}
{#                        <div class="container">#}
{#                            <form method="post" enctype="multipart/form-data" id="downloadForm">#}
{#                                {% csrf\_token %}#}
{#                                {{ form.non\_field\_errors }}#}
{#                                <div class="form-group">#}
{#                                    <label for="id\_category" style="font-size: 18px; margin-bottom: 10px">Категория\*</label>#}
{#                                    <select id="id\_category" name="category" class="form-control" required>#}
{#                                        <option value="">Выберите категорию</option>#}
{#                                        {% for category\_value, category\_label in form.fields.category.choices %}#}
{#                                            <option value="{{ category\_value }}">{{ category\_label }}</option>#}
{#                                        {% endfor %}#}
{#                                    </select>#}
{#                                    <div class="error" id="categoryError"></div>#}
{#                                    {% if form.id\_category.errors %}#}
{#                                    <div class="alert alert-danger alert-dismissible fade show">{{ form.category.errors }}</div>#}
{#                                    {% endif %}#}
{#                                </div>#}
{##}
{#                                <div class="form-group mt-3">#}
{#                                    <label for="id\_start\_date" style="font-size: 18px; margin-bottom: 10px">С какой даты выгружать товары</label>#}
{#                                    <input type="date" id="id\_start\_date" name="start\_date" class="form-control">#}
{#                                </div>#}
{##}
{#                                <div class="form-group mt-3">#}
{#                                    <label for="id\_end\_date" style="font-size: 18px; margin-bottom: 10px">По какую дату выгружать товары</label>#}
{#                                    <input type="date" id="id\_end\_date" name="end\_date" class="form-control">#}
{#                                </div>#}
{#                                <div class="row">#}
{#                                    <div class="col-9"></div>#}
{#                                    <div class="col-3">#}
{#                                        <button type="submit" class="btn btn-dark btn-block mt-4" style="background-color: #1d4d51; color: #a18c0d; margin-left: -10px; margin-bottom: 30px">Выгрузить</button>#}
{#                                    </div>#}
{#                                </div>#}
{#                            </form>#}
{#                        </div>#}
{#                    </div>#}
{#                </div>#}
{#            </div>#}
{#        </div>#}
{#        <div style="height: 350px"></div>#}
{#    </div>#}
{##}
{#    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>#}
{#    <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>#}
{#    <!-- Подключаем Bootstrap JS -->#}
{#    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>#}
{#    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>#}
{#    <script>#}
{#        document.getElementById('downloadForm').addEventListener('submit', function(event) {#}
{#            let valid = true;#}
{#            let category = document.getElementById('category');#}
{#            let categoryError = document.getElementById('categoryError');#}
{##}
{#            if (category.value === '') {#}
{#                valid = false;#}
{#                categoryError.textContent = 'Пожалуйста, выберите категорию.';#}
{#            } else {#}
{#                categoryError.textContent = '';#}
{#            }#}
{##}
{#            if (!valid) {#}
{#                event.preventDefault();#}
{#            }#}
{#        });#}
{#    </script>#}
{#{% endblock %}#}

{#{% extends "base.html" %}#}
{#{% load static %}#}
{##}
{#{% block css %}#}
{#    <link rel="stylesheet" href="{% static "deps/css/my\_footer\_css.css" %}">#}
{#    <style>#}
{#        .error {#}
{#            color: red;#}
{#            margin-top: 5px;#}
{#        }#}
{#    </style>#}
{#{% endblock %}#}
{##}
{#{% block modal\_cart %}#}
{#{% include "includes/cart\_button.html" %}#}
{#{% endblock  %}#}
{##}
{#{% block content %}#}
{#    <div class="mt-3">#}
{#        <h2 class="m-2" style="color: #1d4d51"><strong>{{ content }}</strong></h2>#}
{#        <div class="row mt-5" style="margin-left: 20px">#}
{#            <a class="icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.125rem, 0); color: #1d4d51; text-decoration-color: #1d4d51" href="{% url "admin:index" %}">#}
{#              <img class="bi" src="{% static "deps/icons/profile-br.svg" %}" alt="Catalog Icon" style="width: 40px; height: 40px; margin-bottom: 7px">#}
{#                <h3>Администрирование сайта</h3>#}
{#            </a>#}
{#        </div>#}
{#        <div class="row mt-4" style="margin-left: 20px">#}
{#            <a id="modalButton2" type="button" class="icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.125rem, 0); color: #1d4d51; text-decoration-color: #1d4d51">#}
{#              <img class="bi" src="{% static "deps/icons/excel.svg" %}" alt="Catalog Icon" style="width: 40px; height: 40px; margin-bottom: 7px">#}
{#                <h3>Выгрузить товары</h3>#}
{#            </a>#}
{#        </div>#}
{#        <div class="modal fade" id="exampleModal2" tabindex="-1" aria-labelledby="exampleModalLabel"#}
{#            aria-hidden="true">#}
{#            <div class="modal-dialog modal-dialog-scrollable">#}
{#                <div class="modal-content" style="">#}
{#                    <div class="modal-header" style="border: none; margin-top: 10px; margin-right: 10px">#}
{#                        <button type="button" class="btn-close" data-bs-dismiss="modal"#}
{#                            aria-label="Close"></button>#}
{#                    </div>#}
{#                    <div class="modal-body">#}
{#                        <h3 class="text-center mb-4" style="color: #1d4d51; margin-top: -20px">Выгрузка товаров</h3>#}
{#                        <div class="container">#}
{#                            <form method="post" enctype="multipart/form-data" id="downloadForm">#}
{#                                {% csrf\_token %}#}
{#                                {{ form.non\_field\_errors }}#}
{#                                <div class="form-group">#}
{#                                    <label for="id\_category" style="font-size: 18px; margin-bottom: 10px">Категория\*</label>#}
{#                                    <select id="id\_category" name="category" class="form-control" required>#}
{#                                        <option value="">Выберите категорию</option>#}
{#                                        {% for category\_value, category\_label in form.fields.category.choices %}#}
{#                                            <option value="{{ category\_value }}">{{ category\_label }}</option>#}
{#                                        {% endfor %}#}
{#                                    </select>#}
{#                                    {% if form.category.errors %}#}
{#                                    <div class="alert alert-danger alert-dismissible fade show error" id="categoryError">{{form.category.errors}}</div>#}
{#                                    {% endif %}#}
{#                                    <div class="error" id="categoryError"></div>#}
{#                                </div>#}
{##}
{#                                <div class="form-group mt-3">#}
{#                                    <label for="id\_start\_date" style="font-size: 18px; margin-bottom: 10px">С какой даты выгружать товары</label>#}
{#                                    <input type="date" id="id\_start\_date" name="start\_date" class="form-control">#}
{#                                </div>#}
{##}
{#                                <div class="form-group mt-3">#}
{#                                    <label for="id\_end\_date" style="font-size: 18px; margin-bottom: 10px">По какую дату выгружать товары</label>#}
{#                                    <input type="date" id="id\_end\_date" name="end\_date" class="form-control">#}
{#                                </div>#}
{#                                <div class="row">#}
{#                                    <div class="col-9"></div>#}
{#                                    <div class="col-3">#}
{#                                        <button type="submit" class="btn btn-dark btn-block mt-4" style="background-color: #1d4d51; color: #a18c0d; margin-left: -10px; margin-bottom: 30px">Выгрузить</button>#}
{#                                    </div>#}
{#                                </div>#}
{#                            </form>#}
{#                        </div>#}
{#                    </div>#}
{#                </div>#}
{#            </div>#}
{#        </div>#}
{#        <div style="height: 350px"></div>#}
{#    </div>#}
{##}
{#    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>#}
{#    <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>#}
{#    <!-- Подключаем Bootstrap JS -->#}
{#    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>#}
{#    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>#}
{#    <script>#}
{#        document.getElementById('downloadForm').addEventListener('submit', function(event) {#}
{#            let valid = true;#}
{#            let category = document.getElementById('id\_category');#}
{#            let categoryError = document.getElementById('categoryError');#}
{##}
{#            if (category.value === '') {#}
{#                valid = false;#}
{#                categoryError.textContent = 'Пожалуйста, выберите категорию.';#}
{#            } else {#}
{#                categoryError.textContent = '';#}
{#            }#}
{##}
{#            if (!valid) {#}
{#                event.preventDefault();#}
{#            }#}
{#        });#}
{#    </script>#}
{#{% endblock %}#}

{% extends "base.html" %}
{% load static %}

{% block css %}
`    `<link rel="stylesheet" href="{% static "deps/css/my\_footer\_css.css" %}">
`    `<style>
.error {
`            `color: red;
`            `margin-top: 5px;
`        `}
`    `</style>
{% endblock %}

{% block modal\_cart %}
{% include "includes/cart\_button.html" %}
{% endblock  %}

{% block content %}
`    `<div class="mt-3">
`        `<h2 class="m-2" style="color: #1d4d51"><strong>{{ content }}</strong></h2>
`        `<div class="row mt-5" style="margin-left: 20px">
`            `<a class="icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.125rem, 0); color: #1d4d51; text-decoration-color: #1d4d51" href="{% url "admin:index" %}">
`              `<img class="bi" src="{% static "deps/icons/profile-br.svg" %}" alt="Catalog Icon" style="width: 40px; height: 40px; margin-bottom: 7px">
`                `<h3>Администрирование сайта</h3>
`            `</a>
`        `</div>
`        `<div class="row mt-4" style="margin-left: 20px">
`            `<a id="modalButton2" type="button" class="icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.125rem, 0); color: #1d4d51; text-decoration-color: #1d4d51">
`              `<img class="bi" src="{% static "deps/icons/excel.svg" %}" alt="Catalog Icon" style="width: 40px; height: 40px; margin-bottom: 7px">
`                `<h3>Выгрузить товары</h3>
`            `</a>
`        `</div>
`        `<div class="modal fade" id="exampleModal2" tabindex="-1" aria-labelledby="exampleModalLabel"
`            `aria-hidden="true">
`            `<div class="modal-dialog modal-dialog-scrollable">
`                `<div class="modal-content" style="">
`                    `<div class="modal-header" style="border: none; margin-top: 10px; margin-right: 10px">
`                        `<button type="button" class="btn-close" data-bs-dismiss="modal"
`                            `aria-label="Close"></button>
`                    `</div>
`                    `<div class="modal-body">
`                        `<h3 class="text-center mb-4" style="color: #1d4d51; margin-top: -20px">Выгрузка товаров</h3>
`                        `<div class="container">
`                            `<form method="post" enctype="multipart/form-data" id="downloadForm" novalidate>
`                                `{% csrf\_token %}
`                                `{{ form.non\_field\_errors }}
`                                `<div class="form-group">
`                                    `<label for="id\_category" style="font-size: 18px; margin-bottom: 10px">Категория\*</label>
`                                    `<select id="id\_category" name="category" class="form-control" required>
`                                        `<option value="">Выберите категорию</option>
`                                        `{% for category\_value, category\_label in form.fields.category.choices %}
`                                            `<option value="{{ category\_value }}">{{ category\_label }}</option>
`                                        `{% endfor %}
`                                    `</select>
`                                    `<div class="error" id="categoryError"></div>
`                                `</div>

`                                `<div class="form-group mt-3">
`                                    `<label for="id\_start\_date" style="font-size: 18px; margin-bottom: 10px">С какой даты выгружать товары</label>
`                                    `<input type="date" id="id\_start\_date" name="start\_date" class="form-control">
`                                `</div>

`                                `<div class="form-group mt-3">
`                                    `<label for="id\_end\_date" style="font-size: 18px; margin-bottom: 10px">По какую дату выгружать товары</label>
`                                    `<input type="date" id="id\_end\_date" name="end\_date" class="form-control">
`                                `</div>
`                                `<div class="row">
`                                    `<div class="col-9"></div>
`                                    `<div class="col-3">
`                                        `<button type="submit" class="btn btn-dark btn-block mt-4" style="background-color: #1d4d51; color: #a18c0d; margin-left: -10px; margin-bottom: 30px">Выгрузить</button>
`                                    `</div>
`                                `</div>
`                            `</form>
`                        `</div>
`                    `</div>
`                `</div>
`            `</div>
`        `</div>
`        `<div style="height: 350px"></div>
`    `</div>

`    `<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
`    `<script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
`    `<!-- Подключаем Bootstrap JS -->
`    `<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
`    `<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
`    `<script>
`        `$(document).ready(function() {
`            `$('#downloadForm').on('submit', function(event) {
`                `let valid = true;
`                `let category = $('#id\_category');
`                `let categoryError = $('#categoryError');

`                `if (category.val() === '') {
`                    `valid = false;
`                    `categoryError.text('Пожалуйста, выберите категорию.');
`                `} else {
`                    `categoryError.text('');
`                `}

`                `if (!valid) {
`                    `event.preventDefault();
`                `}
`            `});
`        `});
`    `</script>
{% endblock %}
