from django.contrib import admin
from .models import Customer, FollowUp


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'address')
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'email', 'phone')}),
        ('Address', {'fields': ('address',)}),
        ('Status', {'fields': ('status',)}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('customer', 'follow_up_date', 'next_follow_up_date', 'created_at')
    list_filter = ('follow_up_date', 'created_at')
    search_fields = ('customer__name', 'note')
    fieldsets = (
        ('Customer', {'fields': ('customer',)}),
        ('Follow-up Information', {'fields': ('note', 'follow_up_date', 'next_follow_up_date')}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)
