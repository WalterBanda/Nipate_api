from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^new', views.ProviderView.as_view(), name="createprovider"),
    re_path(r'^service', views.ProviderServiceView.as_view(), name="services"),
    # re_path(r'^service/update/location', views.UpdateProviderServiceLocation.as_view(),
    #         name="service_update_location"),
    re_path(r'^update-location/service', views.updateProviderServiceLocation, name="service_update_location"),
]
