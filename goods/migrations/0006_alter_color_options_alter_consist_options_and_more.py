# Generated by Django 4.2.7 on 2024-06-06 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_color_hex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ('id',), 'verbose_name': 'Цвет', 'verbose_name_plural': 'Цвета'},
        ),
        migrations.AlterModelOptions(
            name='consist',
            options={'ordering': ('id',), 'verbose_name': 'Состав', 'verbose_name_plural': 'Составы'},
        ),
        migrations.AlterModelOptions(
            name='sizes',
            options={'ordering': ('id',), 'verbose_name': 'Размер', 'verbose_name_plural': 'Размеры'},
        ),
    ]
