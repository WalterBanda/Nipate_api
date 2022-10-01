from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^new', views.CreateProvider.as_view(), name="createprovider"),
]
