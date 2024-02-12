# Generated by Django 5.0.1 on 2024-02-12 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_rename_category_id_course_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='hours_forecast',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='time_spent',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='finish_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
