# Generated by Django 4.2.10 on 2024-03-03 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_report_common_issue_report_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='common_issue',
            field=models.CharField(choices=[('1', 'N/A'), ('2', 'Water Fountain Filter'), ('3', 'Clogging in Bathroom'), ('4', 'Bathroom Supply'), ('5', 'Classroom Equipment')], default='1', max_length=2),
        ),
    ]
