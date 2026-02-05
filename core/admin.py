from django.contrib import admin
from .models import Service, Booking, BookingItem, Review

class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_amount', 'status', 'booking_date')
    list_filter = ('status', 'booking_date')
    inlines = [BookingItemInline]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name',)

admin.site.register(Review)