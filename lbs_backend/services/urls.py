from django.urls import path
from .views import requestView, responseView

urlpatterns = [
    # Request Views
    path('provider/', requestView.ServiceProviderView.as_view()),
    path('service-request', requestView.RequestServiceView.as_view()),

    # Response Views
    path('serive-response', responseView.RequestedResponseView.as_view()),
]