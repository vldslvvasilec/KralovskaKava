from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', default='categories/default_bg.jpg')
    background_css = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # Разрешаем значение "Null" для этого поля
        blank=True,  # Разрешаем поле оставлять пустым в формах
        default=None,  # Устанавливаем значение по умолчанию на "None"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    components = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # Разрешаем значение "Null" для этого поля
        blank=True,  # Разрешаем поле оставлять пустым в формах
        default=None,  # Устанавливаем значение по умолчанию на "None"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.creator:
            self.creator = settings.AUTH_USER_MODEL
        super().save(*args, **kwargs)

class Reviews(models.Model):
    name = models.CharField(max_length=100, unique=True)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
