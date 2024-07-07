from modeltranslation.translator import register, TranslationOptions
from modeltranslation.translator import translator
from .models import Category, Product

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'components')


