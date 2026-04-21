from django.contrib import admin
from django.utils.html import format_html
from .models import RenderJob

@admin.register(RenderJob)
class RenderJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'selected_product', 'status', 'output_preview', 'created_at')
    list_filter = ('status', 'selected_product')
    readonly_fields = ('output_preview_large', 'error_message')

    def output_preview(self, obj):
        if obj.output_image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.output_image.url)
        return "Not rendered"
    output_preview.short_description = 'Result'

    def output_preview_large(self, obj):
        if obj.output_image:
            return format_html('<img src="{}" style="width: 300px; height: auto;" />', obj.output_image.url)
        return "Not rendered"
    output_preview_large.short_description = 'Output Preview'
