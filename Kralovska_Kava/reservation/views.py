from django.views import View
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json
from urllib.parse import urlparse
from .models import Restaurant, Reservation
from home.models import Category
from home.serializers import ProductsSerializer
from send_email import send_reservation_email

def header_menu_items():
    categories = Category.objects.prefetch_related('product_set').all()
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
            categories_with_products.append({
                'category': category,
            })
    return categories_with_products

class IndexView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reservation/reservation.html'
    def get(self, request):
        page_title = 'Karlove kofe'
        restaurants = Restaurant.objects.all()
        categories_with_products = header_menu_items()
        template_data = {
            'global_title': page_title,
            'drop_items': categories_with_products,
            'restaurants': restaurants
        }
        return Response(template_data)
        # return render(request, 'reservation/reservation.html', {'restaurants': restaurants})
    

class GetAvailableDatesView(View):
    def get(self, request):
        restaurant_id = request.GET.get('restaurant_id')
        restaurant = Restaurant.objects.get(id=restaurant_id)

        available_dates = Reservation.objects.filter(
            restaurant=restaurant,
            date__gte=now().date()
        ).values_list('date', flat=True).distinct()

        return JsonResponse(list(available_dates), safe=False)

class GetAvailableTimesView(View):
    def get(self, request):
        restaurant_id = request.GET.get('restaurant_id')
        date = request.GET.get('date')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        reservations = Reservation.objects.filter(restaurant=restaurant, date=date)

        # Initialize all time slots
        available_times = {time: 0 for time in self.generate_time_slots(restaurant.opening_time, restaurant.closing_time)}

        # Update count of reserved tables for each time slot
        for reservation in reservations:
            available_times[reservation.time.strftime("%H:%M:%S")] += 1

        # Get time slots with available tables
        times_with_available_tables = [time for time, count in available_times.items() if count < restaurant.tables]
        return JsonResponse(times_with_available_tables, safe=False)

    def generate_time_slots(self, start_time, end_time, interval=60):
        from datetime import datetime, timedelta

        time_slots = []
        current_time = datetime.combine(datetime.today(), start_time)
        end_time = datetime.combine(datetime.today(), end_time)

        while current_time < end_time:
            time_slots.append(current_time.time().strftime("%H:%M:%S"))
            current_time += timedelta(minutes=interval)

        return time_slots


@csrf_exempt
def makeReservationView(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        restaurant_id = data.get('restaurant_id')
        date = data.get('date')
        time = data.get('time')
        name = data.get('name')
        email = data.get('email')
        lang = data.get('lang')

        if not restaurant_id or not date or not time:
            return JsonResponse({'error': 'Все поля обязательны'}, status=400)

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({'error': 'Ресторан не найден'}, status=404)

        # Создание брони
        reservation = Reservation.objects.create(
            restaurant=restaurant,
            date=date,
            time=time,
            name=name,
            email=email
        )

        if reservation:
            print(reservation.restaurant.name)
            print(name)
            print(email)
            print(date)
            print(time)
            send_reservation_email(
                user_email=email,
                user_name=name,
                restaurant_name=reservation.restaurant.name,
                reservation_date=date,
                reservation_time=time,
                user_language=lang)
            request.session['reservation_info'] = {
                'restaurant_name': restaurant.name,
                'name': name,
                'email': email,
                'date': date,
                'time': time,
            }
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Ошибка при создании бронирования'}, status=500)

    return JsonResponse({'error': 'Недопустимый метод запроса'}, status=405)



def reservation_success_view(request):
    page_tittle = 'Karlove kofe'
    categories_with_products = header_menu_items()
    reservation_info = request.session.get('reservation_info', {})
    return render(request, 'reservation/reservation_success.html', {
        'drop_items': categories_with_products,
        'reservation_info': reservation_info,
        'global_title': page_tittle,
    })

def reservation_error_view(request):
    page_tittle = 'Karlove kofe'
    categories_with_products = header_menu_items()
    return render(request, 'reservation/reservation_error.html', {
        'drop_items': categories_with_products,
        'global_title': page_tittle,
    })