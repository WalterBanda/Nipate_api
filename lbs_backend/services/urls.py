from django.urls import re_path
from . import views

urlpatterns = [
    # Request Views
    re_path('^provider', views.ServiceProviderView.as_view()),
    re_path('^service-request', views.RequestServiceView.as_view()),

    # Response Views
    re_path('^service-response', views.RequestedResponseView.as_view()),

    # Adverts Views
    re_path('^advert', views.AdvertView.as_view()),

    # Products Views
    re_path('^category', views.productCategoryView.as_view(), name='categories'),
    re_path('^products', views.productsView.as_view(), name='products'),
    re_path('^allproducts', views.AllProductsView.as_view(), name="allproducts")
]