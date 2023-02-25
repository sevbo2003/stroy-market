from django.contrib import admin
from apps.stroy.models import Category, SubCategory, Product, ProductImage, Size, Color, ProductComment, CommentLike
from modeltranslation.admin import TranslationAdmin


class SubCategoryInline(admin.TabularInline):
    model = SubCategory

class CategoryAdmin(TranslationAdmin):
    inlines = [SubCategoryInline]
    list_display = ('name_uz', 'name_ru', 'slug', 'image')
    search_fields = ('name',)
    readonly_fields = ('slug',)

admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'image', 'category')
    search_fields = ('name',)
    readonly_fields = ('slug',)

admin.site.register(SubCategory, SubCategoryAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage


class SizeInline(admin.TabularInline):
    model = Size


class ColorInline(admin.TabularInline):
    model = Color


class ProductAdmin(TranslationAdmin):
    inlines = [ProductImageInline, ColorInline, SizeInline]
    list_display = ('name', 'in_discount', 'discount_percent', 'price', 'count', 'weight', 'category')
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')


admin.site.register(ProductImage, ProductImageAdmin)


class SizeAdmin(TranslationAdmin):
    list_display = ('name', 'product')


admin.site.register(Size, SizeAdmin)


class ColorAdmin(TranslationAdmin):
    list_display = ('name', 'product')


admin.site.register(Color, ColorAdmin)


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'comment', 'stars', 'created_at')


admin.site.register(ProductComment, ProductCommentAdmin)


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'like', 'dislike')


admin.site.register(CommentLike, CommentLikeAdmin)