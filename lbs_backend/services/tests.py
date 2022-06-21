from django.test import TestCase
from locations.models import TownsModel, CountyModel
from rest_framework.test import APITestCase


class LocationTest(TestCase):

    def setUp(self):
        self.towns_url = "http://127.0.0.1:8000/location/towns/"
        self.counties_url = "http://127.0.0.1:8000/location/counties/"
        
        self.county_a = {"Name": "Nakuru"}
        self.town_a = {"Name": "Rafiki"}

    def create_county(self):
        county = CountyModel(**self.county_a)
        county.save()
        return county
    
    def create_towns(self):
        county = self.create_county()
        towns = TownsModel(**self.towns_a, )