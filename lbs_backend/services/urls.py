from django.urls import re_path
from .views import requestView, responseView, advertView, Products

urlpatterns = [
    # Request Views
    re_path('^provider', requestView.ServiceProviderView.as_view()),
    re_path('^service-request', requestView.RequestServiceView.as_view()),

    # Response Views
    re_path('^service-response', responseView.RequestedResponseView.as_view()),

    # Adverts Views
    re_path('^advert', advertView.AdvertView.as_view()),

    # Products Views
    re_path('^category', Products.productCategoryView.as_view(), name='categories'),
    re_path('^products', Products.productsView.as_view(), name='products'),
    re_path('^allproducts', Products.AllProductsView.as_view(), name="allproducts")
]