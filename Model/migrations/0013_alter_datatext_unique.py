# Generated by Django 3.2.5 on 2022-01-14 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0012_auto_20220114_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datatext',
            name='Unique',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
    ]
