from django.db import models
from django.contrib.auth import get_user_model
from locations.models import (TownsModel)
from users.models import Gender
UserModel = get_user_model()


class ProductCategory(models.Model):
    Name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "ProductCategories"
        verbose_name_plural = "ProductCategories"
    def __str__(self):
        return self.Name

class Product(models.Model):
    CategoryID = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    Name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"

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
class ServiceProvider(models.Model):

    AGE = [
        ('18+', '18+'),
        ('All', 'All'),
        ('10+', '10+'),
        ('16+', '16+'),
    ]
    UserID = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    ProductID = models.ForeignKey(Product, on_delete=models.PROTECT)
    LocationID = models.ForeignKey(TownsModel, on_delete=models.PROTECT, null=True, blank=True)
    GenderID = models.ForeignKey(Gender, on_delete=models.PROTECT,null=True,blank=True)
    AgeBracket = models.CharField(max_length=9, choices=AGE, null=True, blank=True)
    TimeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Providers"
        verbose_name_plural = "Service Providers"
    
    def __str__(self):
        return "%s || %s" % (str(self.id), str(self.UserID))