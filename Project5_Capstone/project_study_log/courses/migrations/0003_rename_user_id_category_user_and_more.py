# Generated by Django 5.0.1 on 2024-02-12 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='term',
            old_name='user_id',
            new_name='user',
        ),
    ]