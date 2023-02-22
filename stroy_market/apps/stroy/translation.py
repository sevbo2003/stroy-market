from modeltranslation.translator import translator, TranslationOptions
from apps.stroy.models import Category, SubCategory, Product, Size, Color


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category, CategoryTranslationOptions)


class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(SubCategory, SubCategoryTranslationOptions)


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'product_type', 'control', 'purpose', 'material', 'xususiyatlari', 'brand', 'sotuvchi', 'description')

translator.register(Product, ProductTranslationOptions)


class SizeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Size, SizeTranslationOptions)


class ColorTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Color, ColorTranslationOptions)
