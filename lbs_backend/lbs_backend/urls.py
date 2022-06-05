from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.site_header = "Location Based Mobile Advertising System Database "
admin.site.index_title = "Applications"

schema_view = get_schema_view(
   openapi.Info(
      title="Nipate data source and API",
      default_version='v1.0',
      description="LBS API's Doc",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="amosditto@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', include('djoser.urls')),
    path('auth', include('djoser.urls.authtoken')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   #  applications urls 
   path('auth/', include('users.urls')),
   path('service/', include("services.urls")),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)