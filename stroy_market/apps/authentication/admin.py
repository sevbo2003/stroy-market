from django.contrib import admin
from apps.authentication.models import User, PhoneToken


admin.site.register(User)


@admin.register(PhoneToken)
class PhoneTokenAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'token', 'created_at', 'expires_at']
    search_fields = ['phone_number', 'token']