from django.db import models


class CountyModel(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'Counties'
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.name


class CenterLocation(models.Model):
    displayName = models.CharField(max_length=250)
    state = models.CharField(max_length=150, null=True, blank=True)
    town = models.CharField(max_length=150, null=True, blank=True)
    suburb = models.CharField(max_length=150, null=True, blank=True)
    road = models.CharField(max_length=150, null=True, blank=True)
    landmark = models.CharField(max_length=150, null=True, blank=True)
    centerBlock = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = "Center Locations"
        verbose_name_plural = "Center Locations"

    def __str__(self):
        return self.displayName
