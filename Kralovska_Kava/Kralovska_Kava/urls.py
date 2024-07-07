from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.urls import path, include
from home.views import change_language
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('reservation/', include('reservation.urls')),
    path('', include('manager.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('change-language/', change_language, name='change_language'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


