from django.urls import path
from locations import views

urlpatterns = [
    path("counties/", views.CountyView.as_view(), name="counties"),
    path("towns/", views.TownsView.as_view(), name="towns"),
]