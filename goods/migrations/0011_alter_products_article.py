# Generated by Django 4.2.7 on 2024-06-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_alter_products_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='article',
            field=models.PositiveIntegerField(default=0, help_text='Артикул товара', unique=True),
        ),
    ]