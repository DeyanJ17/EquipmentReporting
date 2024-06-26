# Generated by Django 4.2.10 on 2024-03-28 21:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0018_report_receive_emails"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="receive_emails",
            field=models.CharField(
                choices=[
                    ("1", "receive all"),
                    ("2", "receive some"),
                    ("3", "receive none"),
                ],
                default="3",
                max_length=25,
            ),
        ),
    ]
