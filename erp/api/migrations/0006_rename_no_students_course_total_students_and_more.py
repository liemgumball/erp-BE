# Generated by Django 5.0 on 2023-12-25 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_paidamount_payment_paid_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='no_students',
            new_name='total_students',
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
