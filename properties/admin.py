from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'formatted_price', 'created_at']
    list_filter = ['location', 'created_at']
    search_fields = ['title', 'description', 'location']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Property Information', {
            'fields': ('title', 'description')
        }),
        ('Pricing & Location', {
            'fields': ('price', 'location')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )