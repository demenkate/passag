from django.db import models
from django.urls import reverse
# from django.contrib.postgres.fields import CITextField


class SizeProductQueryset(models.QuerySet):

    def total_count(self):
        if self:
            return sum(sizeproduct.count for sizeproduct in self)
        return 0


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    tnved = models.CharField(max_length=150, verbose_name='Код тн вэд', null=True)
    filter_size = models.BooleanField(verbose_name='Нужен фильтр для размеров', default=True)
    filter_consist = models.BooleanField(verbose_name='Нужен фильтр для составов', default=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.name


class Sizes(models.Model):
    """Размер товара"""

    RUSSIAN = 1
    INTERNATIONAL = 2

    SIZE_TYPE = [
        (RUSSIAN, 'РОССИЯ'),
        (INTERNATIONAL, 'МЕЖДУНАРОДНЫЙ'),
    ]

    name = models.TextField(help_text='Название')
    type = models.PositiveSmallIntegerField(choices=SIZE_TYPE, default=RUSSIAN)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Color(models.Model):
    """Цвет товара"""

    name = models.TextField(help_text='Название')
    hex = models.TextField(help_text='Цвет в формате hex', null=True)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Consist(models.Model):
    """Состав товара"""

    name = models.TextField(help_text='Название')

    class Meta:
        verbose_name = 'Состав'
        verbose_name_plural = 'Составы'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Country(models.Model):
    """Цвет товара"""

    name = models.TextField(help_text='Название')

    class Meta:
        verbose_name = 'Строна производства'
        verbose_name_plural = 'Строна производства'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.TextField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    category = models.ForeignKey(to=Categories, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    article = models.PositiveIntegerField(default=0, help_text='Артикул товара', unique=True)
    created_at = models.DateField(auto_now_add=True, help_text='Дата добавления', null=True)

    size = models.ManyToManyField(Sizes, through='SizeProductRelation')
    consist = models.ManyToManyField(Consist, related_name='consist')
    color = models.ManyToManyField(Color, related_name='color')
    country = models.ForeignKey(to=Country, on_delete=models.SET_NULL, verbose_name='Страна производства', null=True)


    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)

    def __str__(self):
        return f'{self.name} {self.article}'

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug})

    def display_id(self):
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)

        return self.price


class SizeProductRelation(models.Model):
    """Количество товаров размера"""

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0, help_text='Количество')

    class Meta:
        verbose_name = 'Количество товара размера'
        verbose_name_plural = 'Количество товара размера'

    objects = SizeProductQueryset().as_manager()

    def __str__(self):
        return f"{self.count} {self.size.name} {self.product.name}"
