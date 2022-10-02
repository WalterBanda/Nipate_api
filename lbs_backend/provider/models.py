from django.db import models
from django.contrib.auth import get_user_model
from services.models import Service, WorkingDays
from users.models import Gender, CustomUser
from locations.models import CenterLocation

User = get_user_model()


class ProviderModel(models.Model):
    UserID = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="UserProviderID")
    TimeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Providers"
        verbose_name_plural = "Service Providers"
        ordering = ['TimeStamp']

    def str(self):
        return str(self.UserID)


class ProviderService(models.Model):
    AGE = [
        ('18+', '18+'), ('All', 'All'),
        ('10+', '10+'), ('16+', '16+'),
    ]
    ProviderID = models.ForeignKey(ProviderModel, on_delete=models.CASCADE, related_name="providerID")
    ProviderServiceName = models.CharField(max_length=250)
    ProductID = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="providerProductID")
    CenterLocationID = models.ForeignKey(CenterLocation, on_delete=models.PROTECT, null=True, blank=True,
                                         related_name="providerLocation")
    GenderID = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name="providerGenders")
    AgeBracket = models.CharField(max_length=9, choices=AGE, null=True, blank=True)
    workingDays = models.ManyToManyField(WorkingDays, related_name="workingdays")
    Longitude = models.CharField(max_length=50, blank=True, null=True)
    Lattitude = models.CharField(max_length=50, blank=True, null=True)
    TimeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Provider Services"
        verbose_name_plural = "Provider Services"
        ordering = ['TimeStamp']

    def str(self):
        return "{} | {}".format(str(self.ProviderID), self.ProviderServiceName)
