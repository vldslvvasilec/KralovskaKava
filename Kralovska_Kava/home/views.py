from rest_framework.views import APIView
from django.http import JsonResponse
from django.utils import translation
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.views.generic import DetailView
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
import json
from django.conf import settings
from urllib.parse import urlparse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product, Reviews
from .serializers import MenuSerializer, ProductsSerializer


@csrf_exempt
def change_language(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        language = data.get('language')
        if language in dict(settings.LANGUAGES).keys():
            translation.activate(language)
            response = JsonResponse({'status': 'success', 'message': 'Language changed successfully'})
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
    return JsonResponse({'status': 'failure', 'message': 'Invalid language code'}, status=400)




def sorting_list(lst: list, cols: int) -> list[list]:
    return [lst[i:i + cols] for i in range(0, len(lst), cols)]

class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        page_title = 'Karlove kofe'
        reviews = Reviews.objects.filter(is_active=True)
        categories = Category.objects.prefetch_related('product_set').all()
        drop_menu_serializer = MenuSerializer(categories, many=True)

        categories_with_products = []
        for category in categories:
            products = category.product_set.all()
            if products.exists():
                product_serializer = ProductsSerializer(products, many=True)
                for product in product_serializer.data:
                    # Разбиваем URL изображения на составляющие и берем только базовую часть
                    parsed_url = urlparse(product['image_url'])
                    base_image_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                    product['image_url'] = base_image_url
                sorted_products = sorting_list(product_serializer.data, 4)
                categories_with_products.append({
                    'category': category,
                    'products': sorted_products
                })
        
        template_data = {
            'global_title': page_title,
            'drop_items': categories_with_products,
            'categories_with_products': categories_with_products,
            'reviews' : reviews
        }
        return Response(template_data)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'home/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем объект продукта
        product = self.object
        
        # Устанавливаем заголовок страницы
        context['global_title'] = product.name
        
        # Формируем URL изображения продукта
        parsed_url = urlparse(product.image.url)
        base_image_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        
        # Добавляем URL изображения в контекст
        context['image_url'] = base_image_url
        
        # Получаем категорию текущего продукта
        category = product.category
        
        # Получаем все категории, в которых есть товары
        categories_with_products = []
        categories = Category.objects.filter(product__isnull=False).distinct()
        
        for cat in categories:
            products = cat.product_set.all()[:4]
            categories_with_products.append({
                'category': cat,
                'products': products
            })
        
        # Добавляем drop_items в контекст
        context['drop_items'] = categories_with_products
        
        return context

def add_comment(request):
    if request.method == "POST":
        name = request.POST.get('reviews_name')
        comment = request.POST.get('reviews_comment')
        if name and comment:
            review = Reviews(name=name, comment=comment)
            review.save()
            messages.success(request, _("Thank you for your review"))
            return redirect(reverse('home'))
        else:
            messages.error(request, _("Please fill out all fields"))

    reviews = Reviews.objects.filter(is_active=True)

    return render(request, 'home/home.html')