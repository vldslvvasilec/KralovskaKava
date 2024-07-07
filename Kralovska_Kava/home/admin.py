from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Category, Product, Reviews

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'category', 'date_created', 'is_active')
    list_filter = ('is_active', 'category', 'date_created')
    search_fields = ('name', 'description', 'components', 'creator__username')
    readonly_fields = ('date_created',)


admin.site.register(Reviews)

