from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^counties", views.CountyView.as_view(), name="counties"),
]
