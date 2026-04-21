from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Pharmacy, CustomUser


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_name', 'phone', 'plan', 'is_active', 'created_at')
    list_filter = ('plan', 'is_active')
    search_fields = ('name', 'owner_name', 'phone')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'pharmacy', 'role', 'is_staff')
    list_filter = ('role', 'pharmacy')
    fieldsets = UserAdmin.fieldsets + (
        ('PharmaTrack', {'fields': ('pharmacy', 'role', 'phone')}),
    )
