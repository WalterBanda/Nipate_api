from django.db import models


class CountyModel(models.Model):
    Name = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'Counties'
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.Name


class CenterLocation(models.Model):
    DisplayName = models.CharField(max_length=250)
    State = models.CharField(max_length=150, null=True, blank=True)
    Town = models.CharField(max_length=150, null=True, blank=True)
    Suburb = models.CharField(max_length=150, null=True, blank=True)
    Road = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = "Center Locations"
        verbose_name_plural = "Center Locations"

    def str(self):
        return self.DisplayName
