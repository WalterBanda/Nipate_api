from django.urls import path
from .views import authViews, userRegistration

urlpatterns = [
    path('login', authViews.MyTokenCreateView.as_view(), name="login"),
    path('logout', authViews.MyTokenDestroyView.as_view(), name="logout"),
    path('register/', userRegistration.UserRegister.as_view(), name='register'),
]
# urlpatterns += router.urls
