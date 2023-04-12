from django.contrib import admin
from .models import (
    Recommendation,
    RecommendationProduct,
    RecommentationForCart,
    RecommendationForCartProduct,
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
