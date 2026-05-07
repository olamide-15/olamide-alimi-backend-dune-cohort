from django.contrib import admin
from .models import Product, Category
from django.utils.html import format_html

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'is_available', 'thumbnail']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'is_available']
    list_editable = ['stock', 'is_available']
    ordering = ['created_at']

    actions = ['mark_out_of_stock']

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit:cover; border-radius:4px;">',
                obj.image.url
            )
        return "No Image"
    
    thumbnail.short_description = 'Image'

    def mark_out_of_stock(self, request, queryset):
        queryset.update(stock=0, is_available=False)
        self.message_user(request, 'selected products maked as out of stock.')

    mark_out_of_stock.short_description = 'Mark selected as out of stock'

@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name']


