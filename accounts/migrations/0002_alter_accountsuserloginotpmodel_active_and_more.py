# Generated by Django 4.1.7 on 2023-03-29 06:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsuserloginotpmodel',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='accountsusermodel',
            name='phone_number',
            field=models.IntegerField(default=False, unique=True, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
