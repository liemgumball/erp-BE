# Generated by Django 5.0 on 2023-12-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_payment_balance_payment_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='bill_number',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='created_at',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='paid_amount',
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.CharField(default='math', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
