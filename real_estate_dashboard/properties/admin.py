from django.contrib import admin
from .models import Owner, Property, Deal

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'property_type', 'price', 'is_available')
    list_filter = ('property_type', 'is_available')
    search_fields = ('title', 'address', 'owner__user__username')

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('property', 'deal_type', 'status', 'price', 'start_date')
    list_filter = ('deal_type', 'status')
    search_fields = ('property__title',)