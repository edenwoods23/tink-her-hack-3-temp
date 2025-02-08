from django.contrib import admin
from .models import SkinProfile, Product, Order, OrderItem

# Register your models here.

class SkinProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'summer_skin_type', 'winter_skin_type', 'spring_skin_type')
    search_fields = ('user__username', 'concerns', 'allergies')
    list_filter = ('summer_skin_type', 'winter_skin_type', 'spring_skin_type')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'suitable_for', 'price', 'stock')
    list_filter = ('category', 'suitable_for')
    search_fields = ('name', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status', 'total_amount')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

admin.site.register(SkinProfile, SkinProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
