from rest_framework.test import APITestCase
from django.urls import reverse

from .models import TownsModel, CountyModel


class LocationTests(APITestCase):

    def setUp(self):
        self.counties_get_url = reverse("counties")
        self.towns_get_url = reverse("towns")

        self.county = {"Name": "Nakuru"}
        self.town = {"Name": "Kabarak"}

    def test_create_county(self):
        county = CountyModel(**self.county)
        county.save()
        self.assertEqual(1, county.id)
    
    def test_create_town(self):
        county = CountyModel(**self.county)
        county.save()
        self.assertEqual(1, county.id)
        town = TownsModel(**self.town, County=county)
        town.save()
        self.assertEqual(1, town.id)

    def test_request_counties_api(self):
        county = CountyModel(**self.county)
        county.save()
        self.assertEqual(1, county.id)
        town = TownsModel(**self.town, County=county)
        town.save()
        self.assertEqual(1, town.id)

        response = self.client.get(self.counties_get_url)
        self.assertEqual(response.status_code, 200)
    
    def test_request_towns_api(self):
        county = CountyModel(**self.county)
        county.save()
        self.assertEqual(1, county.id)
        town = TownsModel(**self.town, County=county)
        town.save()
        self.assertEqual(1, town.id)

        response = self.client.get(self.towns_get_url)
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        return super().tearDown()
