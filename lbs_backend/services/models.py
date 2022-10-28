import datetime

from django.db import models
from django.contrib.auth import get_user_model
from users.models import Gender
from locations.models import CountyModel

UserModel = get_user_model()


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Service Categories"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class Service(models.Model):
    categoryID = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="category")
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Services"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name


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


class Advertisement(models.Model):
    from provider.models import ProviderModel
    title = models.CharField(max_length=200, null=True, blank=True)
    providerID = models.ForeignKey(ProviderModel, null=True, on_delete=models.CASCADE)
    serviceID = models.ManyToManyField(Service)
    locationID = models.ForeignKey(CountyModel, on_delete=models.CASCADE)
    genderID = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    startDate = models.DateField(default=datetime.date.today)
    expiryDate = models.DateField()
    noOfMessages = models.IntegerField(null=True, blank=True)

    REQUIRED_FIELDS = ['ProviderID']

    class Meta:
        verbose_name = "Advertisements"
        verbose_name_plural = "Advertisements"

    def __str__(self):
        return str(self.title + " | " + str(self.expiryDate))
