# Generated by Django 4.2.10 on 2024-03-15 03:05

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_report_report_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportsiteuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser equipment_status'),
        ),
        migrations.AlterField(
            model_name='submittedfiles',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=app.models.report_file_path),
        ),
    ]
