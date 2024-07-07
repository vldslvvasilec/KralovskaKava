from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, ProductDetailView, add_comment

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_comment/', add_comment, name='add_comment'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)