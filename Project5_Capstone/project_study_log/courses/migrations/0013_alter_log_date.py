# Generated by Django 5.0.1 on 2024-02-12 21:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_alter_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
