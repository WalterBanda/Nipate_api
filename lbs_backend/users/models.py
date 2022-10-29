from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from locations.models import CountyModel


# ----> Gender Table

class Gender(models.Model):
    name = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Gender'

    def __str__(self):
        return str(self.name)


# ----> User Table

class CustomUser(AbstractBaseUser):
    mobileNumber = models.CharField(max_length=12, unique=True)
    idNumber = models.CharField(max_length=15, null=True, blank=True)
    genderID = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    yearOfBirth = models.DateField(null=True, blank=True)
    firstName = models.CharField(max_length=50, null=True, blank=True)
    middleName = models.CharField(max_length=50, null=True, blank=True)
    surName = models.CharField(max_length=50, null=True, blank=True)
    locationID = models.ForeignKey(CountyModel, on_delete=models.PROTECT, null=True, blank=True)
    adBalance = models.FloatField(default=0, null=True, blank=True)
    dateCreated = models.DateField(auto_now_add=True)
    avatar = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobileNumber'
    REQUIRED_FIELDS = ['idNumber', 'firstName']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return "{} | {}".format(self.mobileNumber, self.firstName)

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
