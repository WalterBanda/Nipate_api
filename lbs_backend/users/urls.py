from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^login', views.LoginJwtToken.as_view(), name="login"),
    re_path('^register', views.UserRegister.as_view(), name='register'),
    re_path('^logout', views.LogOutJwtToken.as_view(), name="logout"),
    re_path(r'^user-details', views.FetchUserDetail.as_view(), name='alldetails'),
]
# urlpatterns += router.urls
