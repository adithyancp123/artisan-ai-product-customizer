from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductView

class ProductViewInline(admin.TabularInline):
    model = ProductView
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'active', 'created_at')
    search_fields = ('name', 'slug')
    list_filter = ('active', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductViewInline]

@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'angle_type', 'preview_base_image', 'print_area_display')
    list_filter = ('angle_type', 'product')
    
    def preview_base_image(self, obj):
        if obj.base_image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.base_image.url)
        return "No image"
    preview_base_image.short_description = 'Base Image'

    def print_area_display(self, obj):
        return f"({obj.print_x}, {obj.print_y}) {obj.print_width}x{obj.print_height}"
    print_area_display.short_description = 'Print Area (X,Y WxH)'
