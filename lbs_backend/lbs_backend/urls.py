from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
# from users import views
# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.views.generic.base import RedirectView


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "User",
                "description": "For using th API you need(mostly) to register as a user. Registering gives you all"
                               "the the non admin access endpoints. After Registration you need to get your JWT "
                               "access token to send requests to the API endpoints"
            },
            {
                "name": "Provider",
                "description": "Provider Endpoints For handling their Functionalities"
            },
            {
                "name": "Services",
                "description": "Services Endpoints: Categories, Services, Products, Advertisements Api's"
            },
            {
                "name": "Services Requests",
                "description": "Services Requests Endpoints: Find service you need done and make a request"
            },
            {
                "name": "Location",
                "description": "Location link to services: Regions/Counties, Centers"
            },
            {
                "name": "Advertisements",
                "description": "Advertise your Services/Products endpoints"
            },
        ]

        return swagger


admin.site.site_header = "Location Based Mobile Advertising System Database "
admin.site.index_title = "Applications"

schema_view = get_schema_view(
    openapi.Info(
        title="Nipate data source and API", default_version='v2.0', description="Nipate API Documentation",
        terms_of_service="https://www.google.com/policies/terms/", contact=openapi.Contact(email="walterkaimurima@gmail.com"),
        license=openapi.License(name="BSD License"),
    ), public=True, permission_classes=[permissions.AllowAny], generator_class=CustomOpenAPISchemaGenerator,
)
urlpatterns = [
    # default project urls
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #  applications urls
    path('auth/', include('users.urls')),
    path('service/', include("services.urls")),
    path('location/', include('locations.urls')),
    path('provider/', include('provider.urls')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
