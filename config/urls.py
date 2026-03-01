"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# 1. URLs that should NEVER have a language prefix (API, Webhooks, JS i18n)
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

# 2. URLs that NEED language prefixes (e.g., /es/admin/, /fr/chat/)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # App inclusions
    path('profile/', include('profiles.urls')),
    path('chat/', include('chat.urls')),
    path('matches/', include('matches.urls')),
    path('explore/', include('explore.urls')),
    path('notifications/', include('notifications.urls')),
    path('membership/', include('membership.urls')),
    path('payment/', include('payments.urls')),
    
    # Homepage / Root apps - Grouped together
    path('', include('company.urls')),
    
    # Optional: Set to False if you want the default language to stay at /path/
    prefix_default_language=True 
)

# 3. Static & Media (Only during development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
