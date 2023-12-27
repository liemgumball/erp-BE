from django.db import models

from custom_users.models import CustomUser

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=1000)
    start_date = models.DateField()
    end_date = models.DateField()
    schedule = models.TextField()
    # Add this field for the number of students
    total_students = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    students = models.ManyToManyField(CustomUser, related_name='courses')

    def __str__(self):
        return self.name


class Payment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    bill_number = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)
    paid_amount = models.PositiveIntegerField(default=0)
    id = models.PositiveIntegerField(primary_key=True)
