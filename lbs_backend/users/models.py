from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# ----> Gender Table

class Gender(models.Model):
    name = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Gender'

    def __str__(self):
        return str(self.id)


# ----> User Table 

class UserManager(BaseUserManager):
    def create_user(self, MobileNumber, IDNumber, FirstName, password=None):
        if not MobileNumber:
            raise ValueError('you must enter your MobileNumber')
        if not IDNumber:
            raise ValueError('you must enter your IDNumber')
        if not FirstName:
            raise ValueError('you must enter your FirstName')

        user = self.model(
            MobileNumber=MobileNumber,
            IDNumber = IDNumber,
            FirstName = FirstName,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, MobileNumber, IDNumber,FirstName, password=None):
        user = self.create_user(MobileNumber, IDNumber,FirstName, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    MobileNumber = models.CharField(max_length=10, unique=True)
    IDNumber = models.CharField(max_length=15, null=True, blank=True)
    GenderID = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    YearOfBirth = models.DateField(null=True, blank=True)
    FirstName = models.CharField(max_length=50, null=True, blank=True)
    MiddleName = models.CharField(max_length=50, null=True, blank=True)
    SurName = models.CharField(max_length=50, null=True, blank=True)
    ADBalance = models.FloatField(default=0, null=True, blank=True)
    DateCreated = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'MobileNumber'
    REQUIRED_FIELDS = ['IDNumber', 'FirstName']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def __str__(self):
        return self.MobileNumber
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin




class WorkingDays(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    days = models.CharField(max_length=9, choices=DAYS_OF_WEEK)

    class Meta:
        verbose_name = "Potential Working Days"
        verbose_name_plural = "Potential Working Days"
    
    def __str__(self):
        return self.days


# -----> Provider Details Model
