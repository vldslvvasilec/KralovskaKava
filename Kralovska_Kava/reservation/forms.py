from django import forms
from .models import Order, Restaurant
from datetime import datetime

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_name', 'order_phone', 'order_email', 'order_day', 'order_time', 'restaurant']

    def clean(self):
        cleaned_data = super().clean()
        order_day = cleaned_data.get('order_day')
        order_time = cleaned_data.get('order_time')
        restaurant = cleaned_data.get('restaurant')

        if order_day and order_time and restaurant:
            if order_day < datetime.today().date():
                self.add_error('order_day', 'Вы не можете выбрать прошедшую дату.')
            if not restaurant.is_time_slot_available(order_day, order_time):
                self.add_error('order_time', 'На выбранное время все столики заняты.')
        return cleaned_data
