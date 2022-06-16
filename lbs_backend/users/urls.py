from django.urls import path
from users.views import authViews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', authViews.MySiteAuthViews)
# router.register('', authViews.MyTokenCreateView, basename="login")
# router.register('', authViews.MyTokenDestroyView, basename="logout")


urlpatterns = [
    path('login', authViews.MyTokenCreateView.as_view(), name="login"),
    path('logout', authViews.MyTokenDestroyView.as_view(), name="logout")
]
urlpatterns += router.urls