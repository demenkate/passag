# Generated by Django 4.2.7 on 2024-06-06 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_country_categories_filter_consist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='goods.categories', verbose_name='Категория'),
        ),
        migrations.RemoveField(
            model_name='products',
            name='country',
        ),
        migrations.AddField(
            model_name='products',
            name='country',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='goods.country', verbose_name='Страна производства'),
        ),
    ]