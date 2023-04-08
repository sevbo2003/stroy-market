from django.contrib import admin
from .models import Recommendation, RecommendationProduct


class RecommendationProductInline(admin.TabularInline):
    model = RecommendationProduct
    extra = 0


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    inlines = [RecommendationProductInline]
