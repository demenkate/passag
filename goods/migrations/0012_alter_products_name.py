# Generated by Django 4.2.7 on 2024-06-07 07:10

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0011_alter_products_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='name',
            field=django.contrib.postgres.fields.citext.CITextField(max_length=150, verbose_name='Название'),
        ),
    ]
