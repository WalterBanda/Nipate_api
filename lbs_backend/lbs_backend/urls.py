from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "Location Based Mobile Advertising System Database "
admin.site.index_title = "Applications"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', include('djoser.urls')),
    path('auth', include('djoser.urls.authtoken')),
    path('auth/', include('users.urls')),

]

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)