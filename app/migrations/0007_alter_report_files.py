# Generated by Django 4.2.10 on 2024-03-04 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_report_common_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='report_files/'),
        ),
    ]
