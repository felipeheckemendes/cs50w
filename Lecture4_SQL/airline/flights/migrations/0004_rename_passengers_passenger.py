# Generated by Django 5.0.1 on 2024-01-29 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_passengers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Passengers',
            new_name='Passenger',
        ),
    ]
