from django.db import models

from custom_users.models import CustomUser

# Create your models here.


class Payment(models.Model):
    created_at = models.DateTimeField()
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bill_number = models.PositiveIntegerField()
    paid = models.PositiveIntegerField()
    balance = models.PositiveIntegerField()
    id = models.PositiveIntegerField(primary_key=True)
