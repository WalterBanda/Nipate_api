from django.urls import re_path
from .views import authViews, userRegistration

urlpatterns = [
    re_path(r'^login', authViews.LoginJwtToken.as_view(), name="login"),
    re_path('^register', userRegistration.UserRegister.as_view(), name='register'),
    re_path('^logout', authViews.LogOutJwtToken.as_view(), name="logout"),
]
# urlpatterns += router.urls
