# Generated by Django 5.0.6 on 2024-07-01 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='energy',
        ),
        migrations.RemoveField(
            model_name='product',
            name='energy_cs',
        ),
        migrations.RemoveField(
            model_name='product',
            name='energy_en',
        ),
        migrations.RemoveField(
            model_name='product',
            name='energy_ru',
        ),
        migrations.RemoveField(
            model_name='product',
            name='energy_uk',
        ),
    ]
