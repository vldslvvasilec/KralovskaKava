from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from urllib.parse import urlparse
from django.http import HttpResponseRedirect
from django.conf import settings
import uuid
from urllib.parse import urljoin


from home.models import Category, Product, Reviews
from reservation.models import Restaurant, Reservation
from home.serializers import ProductsSerializer
from manager.models import Manager
from .forms import ManagerLoginForm

def check_authentication(request):
    if not request.user.is_authenticated:
        return redirect('/manager/login')

def logout_manager_view(request):
    logout(request)
    return redirect('/manager/')

class LoginManagerView(FormView):
    form_class = ManagerLoginForm
    template_name = 'manager/loging_manage.html'
    success_url = reverse_lazy('manager:manager_main')
    page_title = _("manage-loging-tittle")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['global_title'] = self.page_title
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            if user.type_user in ['manager', 'supermanager']:
                login(self.request, user)
                return super().form_valid(form)
            else:
                messages.error(self.request, _("You are not a manager or supermanager"))
                return self.form_invalid(form)
        else:
            messages.error(self.request, _("Invalid username or password"))
            return self.form_invalid(form)

    def form_invalid(self, form):
        return redirect(reverse_lazy('manager:manage_login'))

class ManagerView(LoginRequiredMixin, View):
    login_url = reverse_lazy('manager:manage_login')
    page_title = _('admin_panel')

    def get(self, request, *args, **kwargs):
        if request.user.type_user in ['manager', 'supermanager']:
            return render(request, 'manager/manage_home.html', {'global_title': self.page_title,})
        else:
            messages.error(request, _("You are not authorized to view this page"))
            return redirect(self.login_url)

class ManagerRestauraceView(LoginRequiredMixin, View):
    page_title = _('edit_restaurace_tittle')
    restaurants = Restaurant.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return check_authentication(request) or super().dispatch(request, *args, **kwargs)

    def get(self, request):
        check_authentication(request)
        restourants = Restaurant.objects.all()
        for reservations in restourants:
            reservations.reservation_count = Reservation.objects.filter(restaurant=reservations).count()
        context = {'global_title': self.page_title,
                   'manage_restaurant_restaurants': restourants,
                   'manage_restaurace_error_message': None}
        return render(request, 'manager/details/edit_restaurace.html', context)

    def post(self, request):
        manage_reastaurant_error_message = None
        restaurants = Restaurant.objects.all()

        if 'manage_restaurant_add_restaurant' in request.POST:
            page_title = _('add_restaurace_tittle')
            return render(request, 'manager/details/restaurace_details.html', {
                'restaurants': restaurants,
                'global_title': page_title,
                'page_title': page_title,
            })
        
        elif 'manage_restaurant_edit' in request.POST:
            restaurant_id = request.POST.get('manage_restaurant_restaurant_id')
            restaurant = restaurants.filter(id=restaurant_id).first()
            page_title = f"{_('editing_restaurace_tittle')} {restaurant.name}"
            global_tittle = _('editing_restaurace_tittle')
            reservation_count = Reservation.objects.filter(restaurant=restaurant.id).count()
            return render(request, 'manager/details/restaurace_details.html', {
                'restaurant': restaurant,
                'reservation_count': reservation_count,             
                'global_title': global_tittle,
                'page_title': page_title,
            })
                
        elif 'manage_restaurant_delete_restaurant' in request.POST:
            restaurant_id = request.POST.get('manage_restaurant_restaurant_id')
            if restaurant_id:
                restaurant = Restaurant.objects.get(id=restaurant_id)
                restaurant_name_del = restaurant.name
                restaurant.delete()
                manage_restaurant_error_message = _("restaurant {restaurant_name_del} was successfully deleted.").format(restaurant_name_del=restaurant_name_del)
            else:
                manage_restaurant_error_message = _("No restaurant selected for deletion.")
                restaurants = Restaurant.objects.all()
            for reservations in restaurants:
                reservations.reservation_count = Reservation.objects.filter(restaurant=reservations).count()
            context = {'global_title': self.page_title,
                   'manage_restaurant_restaurants': restaurants,
                   'manage_restaurant_error_message': manage_restaurant_error_message}
        return render(request, 'manager/details/edit_restaurace.html', context)

class ManagerCategoriesView(LoginRequiredMixin, View):
    page_title = _('edit_category_tittle')

    def dispatch(self, request, *args, **kwargs):
        return check_authentication(request) or super().dispatch(request, *args, **kwargs)

    def get(self, request):
        check_authentication(request)
        categories = Category.objects.all()
        for category in categories:
            category.product_count = Product.objects.filter(category=category).count()
        context = {'global_title': self.page_title,
                   'manage_category_categories': categories,
                   'manage_category_error_message': None}
        return render(request, 'manager/details/edit_category.html', context)

    def post(self, request):
        manage_category_error_message = None
        categories = Category.objects.all()

        if 'manage_category_add_category' in request.POST:
            page_title = _('add_category_tittle')
            return render(request, 'manager/details/category_details.html', {
                'category': categories,
                'global_title': page_title,
                'page_title': page_title,
                'languages': settings.LANGUAGES,
            })
        
        elif 'manage_category_edit' in request.POST:
            category_id = request.POST.get('manage_category_category_id')
            category = categories.filter(id=category_id).first()
            page_title = f"{_('editing_category_tittle')} {category.name}"
            global_tittle = _('editing_category_tittle')
            category_names = {lang_code: getattr(category, f'name_{lang_code}', '') for lang_code, _ in settings.LANGUAGES}
            for category_count in categories:
                category.product_count = Product.objects.filter(category=category).count()
            return render(request, 'manager/details/category_details.html', {
                'category': category,
                'category_count': category_count,
                'category_names': category_names,
                'global_title': global_tittle,
                'page_title': page_title,
                'languages': settings.LANGUAGES,
            })
                
        elif 'manage_category_delete_category' in request.POST:
            category_id = request.POST.get('manage_category_category_id')
            if category_id:
                category = Category.objects.get(id=category_id)
                category_name_del = category.name
                category.delete()
                manage_category_error_message = _("category {category_name_del} was successfully deleted.").format(category_name_del=category_name_del)
            else:
                manage_category_error_message = _("No category selected for deletion.")
                categories = Category.objects.all()
            for category in categories:
                category.product_count = Product.objects.filter(category=category).count()
            context = {'global_title': self.page_title,
                   'manage_category_categories': categories,
                   'manage_category_error_message': manage_category_error_message}
        return render(request, 'manager/details/edit_category.html', context)

class ManagerProductsView(LoginRequiredMixin, View):
    page_title = _('edit_products_tittle')

    def dispatch(self, request, *args, **kwargs):
        return check_authentication(request) or super().dispatch(request, *args, **kwargs)

    def get(self, request):
        check_authentication(request)
        products = Product.objects.all()
        context = {'global_title': self.page_title,
                   'media_url' : settings.MEDIA_URL,
                   'manage_products': products,
                   'manage_products_error_message': None}
        return render(request, 'manager/details/edit_product.html', context)

    def post(self, request):
        manage_products_error_message = None
        products = Product.objects.all()

        if 'manage_products_add_product' in request.POST:
            page_title = _('add_product_tittle')
            product_category = Category.objects.all()
            return render(request, 'manager/details/product_details.html', {
                'products': products,
                'global_title': page_title,
                'page_title': page_title,
                'product_category': product_category,
                'languages': settings.LANGUAGES,
            })
        
        elif 'manage_product_edit' in request.POST:
            product_id = request.POST.get('manage_product_product_id')
            product = products.filter(id=product_id).first()
            product_category = Category.objects.all()
            page_title = f"{_('editing_product_tittle')} {product.name}"
            global_tittle = _('editing_product_tittle')
            product_names = {lang_code: getattr(product, f'name_{lang_code}', '') for lang_code, _ in settings.LANGUAGES}
            product_descriptions = {lang_code: getattr(product, f'description_{lang_code}', '') for lang_code, _ in settings.LANGUAGES}
            product_components = {lang_code: getattr(product, f'components_{lang_code}', '') for lang_code, _ in settings.LANGUAGES}
            return render(request, 'manager/details/product_details.html', {
                'product': product,
                'product_names': product_names,
                'product_descriptions': product_descriptions,
                'product_components': product_components,
                'product_category': product_category,
                'global_title': global_tittle,
                'page_title': page_title,
                'languages': settings.LANGUAGES,
            })
                
        elif 'manage_product_delete_product' in request.POST:
            product_id = request.POST.get('manage_product_product_id')
            products = Product.objects.all()
            if product_id:
                product = Product.objects.get(id=product_id)
                product_name_del = product.name
                product.delete()
                manage_products_error_message = _("product {product_name_del} was successfully deleted.").format(product_name_del=product_name_del)
            else:
                manage_products_error_message = _("No product selected for deletion.")

            context = {'global_title': self.page_title,
                    'media_url' : settings.MEDIA_URL,
                    'manage_products': products,
                    'manage_products_error_message': manage_products_error_message}
        return render(request, 'manager/details/edit_product.html', context)

class ManagerManagersView(LoginRequiredMixin, View):
    page_title = _('edit_managers_tittle')
    managers = Manager.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return check_authentication(request) or super().dispatch(request, *args, **kwargs)

    def get(self, request):
        check_authentication(request)
        managers = Manager.objects.all()
        for manager in managers:
            manager.product_count = Product.objects.filter(creator=manager).count()
        context = {'global_title': self.page_title,
                   'manage_managers_managers': managers,
                   'manage_managers_error_message': None}
        return render(request, 'manager/details/edit_managers.html', context)

    def post(self, request):
        manage_managers_error_message = None
        managers = Manager.objects.all()

        if 'manage_managers_add_manager' in request.POST:
            page_title = _('add_manager_tittle')
            user_types = Manager._meta.get_field('type_user').choices
            return render(request, 'manager/details/managers_details.html', {
                'managers': managers,
                'user_types' : user_types,
                'global_title': page_title,
                'page_title': page_title,
            })
        
        elif 'manage_managers_edit' in request.POST:
            manager_id = request.POST.get('manage_managers_manager_id')
            manager = managers.filter(id=manager_id).first()
            page_title = f"{_('editing_manager_tittle')} {manager.username}"
            global_tittle = _('editing_manager_tittle')
            products_count = Product.objects.filter(creator=manager).count()
            user_types = Manager._meta.get_field('type_user').choices
            return render(request, 'manager/details/managers_details.html', {
                'manager': manager,
                'user_types' : user_types,
                'products_count': products_count,
                'global_title': global_tittle,
                'page_title': page_title,
            })
                
        elif 'manage_managers_delete_manager' in request.POST:
            manager_id = request.POST.get('manage_managers_manager_id')
            if manager_id:
                manager = Manager.objects.get(id=manager_id)
                manager_name_del = manager.username
                manager.delete()
                manage_managers_error_message = _("manager {manager_name_del} was successfully deleted.").format(manager_name_del=manager_name_del)
            else:
                manage_managers_error_message = _("No managers selected for deletion.")
                managers = Manager.objects.all()
            for manager in managers:
                manager.product_count = Product.objects.filter(creator=manager).count()
            context = {'global_title': self.page_title,
                   'manage_managers_managers': managers,
                   'manage_managers_error_message': manage_managers_error_message}
        return render(request, 'manager/details/edit_managers.html', context)

class ManagerReservationsView(LoginRequiredMixin, View):
    page_title = _('edit_reservations_tittle')
    managers = Manager.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return check_authentication(request) or super().dispatch(request, *args, **kwargs)

    def get(self, request):
        check_authentication(request)
        reservations = Reservation.objects.all()
        context = {'global_title': self.page_title,
                   'manage_reservations_reservations': reservations,
                   'manage_reservations_error_message': None}
        return render(request, 'manager/details/edit_reservace.html', context)

    def post(self, request):
        manage_reservations_error_message = None
        reservations = Reservation.objects.all()
                
        if 'manage_reservations_delete_reservation' in request.POST:
            reservation_id = request.POST.get('manage_reservations_reservation_id')
            if reservation_id:
                reservation = Reservation.objects.get(id=reservation_id)
                reservation_name_del = reservation.name
                reservation.delete()
                manage_reservations_error_message = _("Reservation for {reservation_name_del} was successfully deleted.").format(reservation_name_del=reservation_name_del)
            else:
                manage_reservations_error_message = _("No reservation selected for deletion.")
                reservations = Reservation.objects.all()
            context = {'global_title': self.page_title,
                   'manage_reservations_reservations': reservations,
                   'manage_reservations_error_message': manage_reservations_error_message}
        return render(request, 'manager/details/edit_reservace.html', context)

class ManagerReviewsView(LoginRequiredMixin, View):
    page_title = _('edit_reviews_tittle')
    reviews = Reviews.objects.all()

    def dispatch(self, request, *args, **kwargs):
        return check_authentication(request) or super().dispatch(request, *args, **kwargs)

    def get(self, request):
        check_authentication(request)
        reviews = Reviews.objects.all()
        context = {'global_title': self.page_title,
                   'manage_reviews': reviews,
                   'manage_reviews_error': None}
        return render(request, 'manager/details/edit_reviews.html', context)

    def post(self, request):
        manage_reviews_error = None
        reviews = Reviews.objects.all()
                
        if 'manage_reviews_delete_review' in request.POST:
            review_id = request.POST.get('manage_reviews_review_id')
            if review_id:
                review = Reviews.objects.get(id=review_id)
                review_name_del = review.name
                review.delete()
                manage_reviews_error = _("Comment for {review_name_del} was successfully deleted.").format(review_name_del=review_name_del)
            else:
                manage_reviews_error = _("No Comments selected for deletion.")
                reviews = Reservation.objects.all()
            context = {'global_title': self.page_title,
                   'manage_reviews': reviews,
                   'manage_reviews_error': manage_reviews_error}
        return render(request, 'manager/details/edit_reviews.html', context)

def back_details(request):
    if request.method == 'POST':
        return_url = request.POST.get('return_url')
        return HttpResponseRedirect(return_url)
    
def create_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id) if category_id else Category()

        for lang_code, lang_name in settings.LANGUAGES:
            field_name = f'name_{lang_code}'
            if field_name in request.POST:
                setattr(category, field_name, request.POST.get(field_name))

        category.background_css = request.POST.get('background_css')
        category.is_active = 'is_active' in request.POST

        if request.user.is_authenticated:
            category.creator = request.user

        category.save()
        
        return_url = request.POST.get('return_url', '/')
        return HttpResponseRedirect(return_url)
    return render(request, 'manager/details/edit_category.html')

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)    
    if request.method == 'POST':
        # Обновляем поля названий на разных языках
        for lang_code in settings.LANGUAGES:
            field_name = f'name_{lang_code[0]}'
            if field_name in request.POST:
                setattr(category, field_name, request.POST.get(field_name))


        # Обновляем CSS для фона и активность категории
        category.background_css = request.POST.get('background_css')
        category.is_active = 'is_active' in request.POST

        # Устанавливаем создателя категории, если пользователь аутентифицирован
        if request.user.is_authenticated:
            category.creator = request.user

        # Обновляем время последнего обновления категории
        category.date_created = timezone.now()
        category.save()
        # Перенаправляем пользователя на указанный URL в форме или на главную страницу
        return_url = request.POST.get('return_url', '/')
        return HttpResponseRedirect(return_url)
    
    return render(request, 'manager/details/edit_category.html', {'category': category})

def create_restaurant(request):
    if request.method == 'POST':
        restaurace_id = request.POST.get('restaurace_id')
        restaurace = get_object_or_404(Restaurant, id=restaurace_id) if restaurace_id else Restaurant()

        restaurace.name = request.POST.get('name_reataurant')
        restaurace.tables = request.POST.get('tables_reataurant')
        restaurace.opening_time = request.POST.get('open_restaurant')
        restaurace.closing_time = request.POST.get('close_restaurant')
        restaurace.is_active = 'is_active' in request.POST

        if request.user.is_authenticated:
            restaurace.creator = request.user

        restaurace.save()
        
        return_url = request.POST.get('return_url', '/')
        return HttpResponseRedirect(return_url)
    return render(request, 'manager/details/edit_restaurace.html')

def update_restaurant(request, restaurant_id):
    restaurace = get_object_or_404(Restaurant, id=restaurant_id)    
    if request.method == 'POST':

        restaurace.name = request.POST.get('name_reataurant')
        restaurace.tables = request.POST.get('tables_reataurant')
        restaurace.opening_time = request.POST.get('open_restaurant')
        restaurace.closing_time = request.POST.get('close_restaurant')
        restaurace.is_active = 'is_active' in request.POST

        # Устанавливаем создателя категории, если пользователь аутентифицирован
        if request.user.is_authenticated:
            restaurace.creator = request.user

        restaurace.save()
        # Перенаправляем пользователя на указанный URL в форме или на главную страницу
        return_url = request.POST.get('return_url', '/')
        return HttpResponseRedirect(return_url)
    
    return render(request, 'manager/details/edit_restaurace.html', {'restaurace': restaurace})

def create_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id) if product_id else Product()

        new_category_id = uuid.uuid4()
        product.id = int(new_category_id.hex[:3], 16)

        for lang_code, lang_name in settings.LANGUAGES:
            field_name = f'name_{lang_code}'
            description_name = f'description_{ lang_code }'
            components_name = f'components_{ lang_code }'
            if field_name in request.POST:
                setattr(product, field_name, request.POST.get(field_name))
            if description_name in request.POST:
                setattr(product, description_name, request.POST.get(description_name))
            if components_name in request.POST:
                setattr(product, components_name, request.POST.get(components_name))

        category_id = request.POST.get('product-category')
        if category_id:
            category = Category.objects.get(pk=category_id)
            product.category = category

        product.image = request.POST.get('product_id')
        image = request.FILES.get('product-img')
        if image:
            product.image = request.FILES.get('product-img')
        else:
            product.image = request.POST.get('product-img-exist').split('/')[1]

        product.is_active = 'is_active' in request.POST

        if request.user.is_authenticated:
            product.creator = request.user

        product.save()
        
        return_url = request.POST.get('return_url', '/')
        return HttpResponseRedirect(return_url)
    
    product_categories = Category()
    context = {
        'product_category': product_categories,
    }
    return render(request, 'manager/details/edit_product.html', context)

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id) 
    if request.method == 'POST':
        for lang_code in settings.LANGUAGES:
            field_name = f'name_{lang_code}'
            description_name = f'description_{ lang_code }'
            components_name = f'components_{ lang_code }'
            if field_name in request.POST:
                setattr(product, field_name, request.POST.get(field_name))
            if description_name in request.POST:
                setattr(product, description_name, request.POST.get(description_name))
            if components_name in request.POST:
                setattr(product, components_name, request.POST.get(components_name))

        category_id = request.POST.get('product-category')
        if category_id:
            category = Category.objects.get(pk=category_id)
            product.category = category

        product.image = request.FILES.get('product-img')

        product.is_active = 'is_active' in request.POST

        if request.user.is_authenticated:
            product.creator = request.user

        # product.date_created = timezone.now()
        
        product.save()

        return_url = request.POST.get('return_url', '/')
        return HttpResponseRedirect(return_url)
    
    product_categories = Category()
    context = {
        'product_category': product_categories,
    }
    return render(request, 'manager/details/edit_product.html')

def create_managers(request):
    if request.method == 'POST':
        manager_id = request.POST.get('manager_id')
        manager = get_object_or_404(Manager, id=manager_id) if manager_id else Manager()

        manager.username = request.POST.get('name_manager')
        manager.email = request.POST.get('managers_email')
        manager.first_name = request.POST.get('managers_first_name')
        manager.last_name = request.POST.get('managers_last_name')
        manager.type_user = request.POST.get('manager_type_user')

        manager_password = request.POST.get('managers_password')
        if manager_password:
            manager.set_password(manager_password)

        manager.is_active = 'is_active' in request.POST
        manager.save()
        
        return_url = request.POST.get('return_url', '/')
        return HttpResponseRedirect(return_url)
    return render(request, 'manager/details/edit_managers.html')

def update_managers(request, manager_id):
    manager= get_object_or_404(Manager, id=manager_id)    
    if request.method == 'POST':

        manager.username = request.POST.get('name_manager')
        manager.email = request.POST.get('managers_email')
        manager.first_name = request.POST.get('managers_first_name')
        manager.last_name = request.POST.get('managers_last_name')
        manager.type_user = request.POST.get('manager_type_user')
        
        manager_password = request.POST.get('managers_password')
        if manager_password:
            manager.set_password(manager_password)

        manager.is_active = 'is_active' in request.POST
        manager.save()

        return_url = request.POST.get('return_url', '/')
        return HttpResponseRedirect(return_url)
    
    return render(request, 'manager/details/edit_managers.html')
