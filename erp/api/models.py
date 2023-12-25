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


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    schedule = models.TextField()
    # Add this field for the number of students
    no_students = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
