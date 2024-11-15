from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

# URL Configuration for the Structuring_AI project
urlpatterns = [
    # Admin panel URL
    path("admin/", admin.site.urls),

    # Include URLs from the 'app' app
    path('', include('app.urls')),  # Root URL routes to 'app' app's URLs
]

# Add static file URLs (for development)
urlpatterns += staticfiles_urlpatterns()

# Serve media files during development (only in DEBUG mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
