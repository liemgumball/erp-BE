# Generated by Django 5.0 on 2023-12-25 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='code',
        ),
    ]
