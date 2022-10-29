from django.db import models
from django.contrib.auth import get_user_model
from users.models import Gender, CustomUser
from locations.models import CenterLocation, CountyModel

User = get_user_model()


class ProviderModel(models.Model):
    userID = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="UserProviderID")
    countyID = models.ForeignKey(CountyModel, on_delete=models.CASCADE, related_name="provider_county", null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Providers"
        verbose_name_plural = "Service Providers"
        ordering = ['timeStamp']

    def __str__(self):
        return str(self.userID)


class ProviderService(models.Model):
    from services.models import Service, WorkingDays
    AGE = [
        ('18+', '18+'), ('All', 'All'),
        ('10+', '10+'), ('16+', '16+'),
    ]
    providerID = models.ForeignKey(ProviderModel, on_delete=models.CASCADE, related_name="providerID")
    serviceTitle = models.CharField(max_length=250)
    productID = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="providerProductID")
    centerLocationID = models.ForeignKey(CenterLocation, on_delete=models.PROTECT, null=True, blank=True,
                                         related_name="providerLocation")
    serviceDescription = models.TextField(null=True, blank=True)
    genderID = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name="providerGenders")
    ageBracket = models.CharField(max_length=9, choices=AGE, null=True, blank=True)
    workingDays = models.ManyToManyField(WorkingDays, related_name="workingdays")
    longitude = models.CharField(max_length=50, blank=True, null=True)
    lattitude = models.CharField(max_length=50, blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Provider Services"
        verbose_name_plural = "Provider Services"
        ordering = ['-timeStamp']

    def __str__(self):
        return "{} | {}".format(str(self.providerID), self.serviceTitle)


class ServiceRequest(models.Model):
    userID = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_requesting')
    providerServiceID = models.ForeignKey(ProviderService, on_delete=models.CASCADE)
    centerLocationID = models.ForeignKey(CenterLocation, on_delete=models.DO_NOTHING, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    requestText = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Services Requests"
        verbose_name_plural = "Services Requests"
        ordering = ['-timeStamp']

    def __str__(self):
        return self.userID.firstName + " | " + self.providerServiceID.serviceTitle


class ServiceResponse(models.Model):
    serviceRequestID = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    responseText = models.TextField(null=True, blank=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Services Responses"
        verbose_name_plural = "Services Responses"
        ordering = ['-timeStamp']

    def __str__(self):
        return str(self.serviceRequestID)
