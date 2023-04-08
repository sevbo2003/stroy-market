from django.contrib import admin
from .models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ('image', 'is_active', 'width', 'height')
    list_filter = ('is_active',)
    list_display_links = ('image',)
    list_editable = ('is_active', 'width', 'height')

    


admin.site.register(Banner, BannerAdmin)