from django.urls import path
from .views import requestView, responseView, advertView

urlpatterns = [
    # Request Views
    path('provider/', requestView.ServiceProviderView.as_view()),
    path('service-request/', requestView.RequestServiceView.as_view()),

    # Response Views
    path('service-response/', responseView.RequestedResponseView.as_view()),

    # Adverts Views
    path('advert/', advertView.AdvertView.as_view())
]