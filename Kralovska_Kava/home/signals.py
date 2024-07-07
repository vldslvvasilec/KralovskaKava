from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Category, Product

@receiver(post_delete, sender=Category)
def delete_category_image(sender, instance, **kwargs):
    if instance.image and instance.image.name != 'categories/default_bg.jpg':
        instance.image.delete(save=False)

@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
