from rest_framework import serializers
from products.models import Product, ProductView
from renderer.models import RenderJob

class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductView
        fields = ['id', 'angle_type', 'base_image', 'print_x', 'print_y', 'print_width', 'print_height']

class ProductSerializer(serializers.ModelSerializer):
    views = ProductViewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'active', 'views']

class RenderJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenderJob
        fields = ['id', 'uploaded_design', 'selected_product', 'selected_view', 'status', 'output_image', 'error_message', 'created_at']
        read_only_fields = ['status', 'output_image', 'error_message']

class RenderJobStatusSerializer(serializers.ModelSerializer):
    output_image_url = serializers.SerializerMethodField()

    class Meta:
        model = RenderJob
        fields = ['id', 'status', 'progress', 'output_image', 'output_image_url', 'error_message', 'updated_at']

    def get_output_image_url(self, obj):
        if obj.output_image:
            return obj.output_image.url
        return None
