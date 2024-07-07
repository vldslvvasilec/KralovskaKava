from django.conf import settings
from django.db import models
from django.utils import timezone

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    tables = models.PositiveIntegerField(default=1)
    opening_time = models.TimeField(default="09:00:00")  # Время открытия ресторана
    closing_time = models.TimeField(default="19:00:00")  # Время закрытия ресторана
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # Разрешаем значение "Null" для этого поля
        blank=True,  # Разрешаем поле оставлять пустым в формах
        default=None,  # Устанавливаем значение по умолчанию на "None"
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.restaurant.name} - {self.date} at {self.time}'
