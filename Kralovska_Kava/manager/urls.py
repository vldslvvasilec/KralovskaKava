from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ManagerView, LoginManagerView, ManagerCategoriesView, ManagerProductsView, ManagerRestauraceView, ManagerManagersView, ManagerReservationsView, ManagerReviewsView, logout_manager_view, back_details, create_category, update_category, create_product, update_product, create_restaurant, update_restaurant, create_managers, update_managers

app_name = 'manager'

urlpatterns = [
    path('manager/', ManagerRestauraceView.as_view(), name='manager_main'),
    path('manager/login', LoginManagerView.as_view(), name='manage_login'),
    path('manager/logout', logout_manager_view, name='logout_manager'),

    path('menu_restaurants', ManagerRestauraceView.as_view(), name='menu_restaurants'),
    path('menu_categories', ManagerCategoriesView.as_view(), name='menu_categories'),
    path('menu_products', ManagerProductsView.as_view(), name='menu_products'),
    path('menu_managers', ManagerManagersView.as_view(), name='menu_managers'),
    path('menu_reservations', ManagerReservationsView.as_view(), name='menu_reservations'),
    path('menu_comments', ManagerReviewsView.as_view(), name='menu_comments'),

    path('back_details/', back_details, name='back_details'),

    path('create_category/', create_category, name='create_category'),
    path('update_category/<int:category_id>/', update_category, name='update_category'),

    path('create_product/', create_product, name='create_product'),
    path('update_product/<int:product_id>/', update_product, name='update_product'),

    path('create_restaurant/', create_restaurant, name='create_restaurant'),
    path('update_restaurant/<int:restaurant_id>/', update_restaurant, name='update_restaurant'),

    path('create_manager/', create_managers, name='create_manager'),
    path('update_manager/<int:manager_id>/', update_managers, name='update_manager'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)