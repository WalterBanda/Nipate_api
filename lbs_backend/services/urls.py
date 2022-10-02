from django.urls import re_path
from . import views

urlpatterns = [

    # Services Views
    re_path('^category', views.ServicesCategoryView.as_view(), name='categories'),
    re_path('^services', views.ServicesView.as_view(), name='services'),
    re_path('^allservices', views.AllServicesView.as_view(), name="allproducts")
]