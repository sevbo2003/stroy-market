from modeltranslation.translator import translator, TranslationOptions
from apps.stroy.models import Category, SubCategory


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category, CategoryTranslationOptions)


class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(SubCategory, SubCategoryTranslationOptions)
