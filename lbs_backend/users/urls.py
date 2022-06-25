from django.urls import path
from users.views import authViews, userRegistration
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('register', authViews.MySiteAuthViews, basename="register_user")


urlpatterns = [
    path('login', authViews.MyTokenCreateView.as_view(), name="login"),
    path('logout', authViews.MyTokenDestroyView.as_view(), name="logout"),
    path('registration/', userRegistration.userRegistration.as_view(), name='user'),
]
# urlpatterns += router.urls