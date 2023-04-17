from django.contrib import admin
from .models import (
    Recommendation,
    RecommendationProduct,
    RecommentationForCart,
    RecommendationForCartProduct,
    RecommendationForProductDetail,
    RecommendationForProductDetailProduct,
    RecommendationForCategory,
    RecommendationForCategoryProduct,
)


class RecommendationProductInline(admin.TabularInline):
    model = RecommendationProduct
    extra = 0


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    inlines = [RecommendationProductInline]


class RecommendationForCartProductInline(admin.TabularInline):
    model = RecommendationForCartProduct
    extra = 0


@admin.register(RecommentationForCart)
class RecommentationForCartAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    inlines = [RecommendationForCartProductInline]


class RecommendationForProductDetailProductInline(admin.TabularInline):
    model = RecommendationForProductDetailProduct
    extra = 0


@admin.register(RecommendationForProductDetail)
class RecommendationForProductDetailAdmin(admin.ModelAdmin):
    list_display = ("title", "product", "created_at", "updated_at")
    inlines = [RecommendationForProductDetailProductInline]


class RecommendationForCategoryProductInline(admin.TabularInline):
    model = RecommendationForCategoryProduct
    extra = 0


@admin.register(RecommendationForCategory)
class RecommendationForCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "updated_at")
    inlines = [RecommendationForCategoryProductInline]