from django.contrib import admin
from apps.stroy.models import Category, SubCategory
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    list_display = ('name_uz', 'name_ru', 'slug', 'image')
    search_fields = ('name',)
    readonly_fields = ('slug',)

admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'image', 'category')
    search_fields = ('name',)
    readonly_fields = ('slug',)

admin.site.register(SubCategory, SubCategoryAdmin)
