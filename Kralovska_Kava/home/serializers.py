from rest_framework import serializers
from .models import Category, Product

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'background_css']

class ProductsSerializer(serializers.ModelSerializer):
    category = MenuSerializer()
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'image_url', 'category', 'description', 'components']
    
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None
