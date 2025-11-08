from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/customer/', include('apps.customer.urls')),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include('apps.vehicle.urls')),
    path('api/', include('apps.booking.urls')),

    path('reports/', include('apps.report.urls', namespace='report')),
]



# Only in development stage
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)