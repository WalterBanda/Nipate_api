from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^counties", views.CountyView.as_view(), name="counties"),
    re_path(r"^towns", views.TownsView.as_view(), name="towns"),
    re_path(r"^locations", views.LocationApi.as_view(), name="locations"),
]
