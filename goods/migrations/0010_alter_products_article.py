# Generated by Django 4.2.7 on 2024-06-06 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_alter_products_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='article',
            field=models.CharField(help_text='Артикул товара', max_length=150, unique=True),
        ),
    ]
