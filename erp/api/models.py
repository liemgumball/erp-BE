from django.db import models
from datetime import timedelta
from custom_users.models import CustomUser

# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(blank=True, max_length=1000)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    schedule = models.TextField()
    total_students = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    students = models.ManyToManyField(
        CustomUser, related_name='courses', blank=True, null=True)
    video = models.CharField(max_length=255, default='kAM1PulT0Ns')

    def __str__(self):
        return self.name


class Payment(models.Model):
    paid_at = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Calculate end_date four weeks after start_date
        if self.start_date:
            self.end_date = self.start_date + timedelta(weeks=4)

        # Set paid to True if paid_at is provided
        if self.paid_at:
            self.paid = True

        super().save(*args, **kwargs)


class Report(models.Model):
    student = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self, *args, **kwargs):
        return f"{self.student}: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
