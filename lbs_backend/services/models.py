from django.db import models
from django.contrib.auth import get_user_model
from users.models import Gender

UserModel = get_user_model()


class ServiceCategory(models.Model):
    Name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Product Categories"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.Name


class Service(models.Model):
    CategoryID = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="category")
    Name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"


class WorkingDays(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
        ('Friday', 'Friday'), ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    days = models.CharField(max_length=9, choices=DAYS_OF_WEEK)

    class Meta:
        verbose_name = "Potential Working Days"
        verbose_name_plural = "Potential Working Days"

    def __str__(self):
        return self.days
