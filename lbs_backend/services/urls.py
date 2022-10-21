from django.urls import re_path
from . import views

urlpatterns = [

    # Services Views
    re_path('^category', views.ServicesCategoryView.as_view(), name='categories'),
    re_path('^services', views.ServicesView.as_view(), name='services'),
    re_path('^allservices', views.AllServicesView.as_view(), name="allproducts"),
    re_path('^advert', views.AdvertisementView.as_view(), name="adverts"),
    re_path('^request', views.ServiceRequestView.as_view(), name="request"),
    re_path('^response', views.ServiceResponseView.as_view(), name="responses"),
    re_path('^request/provider', views.getRequestsByProvider, name="get_requests_provider"),
    re_path('^request/client', views.getRequestsByClient, name="get_requests_client"),
    re_path('^request/client/noresponse', views.getRequestNotRespondedByUser, name="get_requests_client_zero"),
    re_path('^request/provider/noresponse', views.getRequestNotRespondedByProvider, name="get_requests_provider_zero"),
    re_path('^response/client', views.getResponseByUser, name="get_response_client"),
    re_path('^response/provider', views.getResponsesByProvider, name="get_response_provider"),
]