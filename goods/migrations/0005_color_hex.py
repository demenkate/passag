# Generated by Django 4.2.7 on 2024-06-06 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_products_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='hex',
            field=models.TextField(help_text='Цвет в формате hex', null=True),
        ),
    ]