from django.urls import path
from .views import requestView

urlpatterns = [
    path('provider/', requestView.ServiceProviderView.as_view()),
    path('service-request', requestView.RequestServiceView.as_view()),
]