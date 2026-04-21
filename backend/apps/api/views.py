from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from products.models import Product, ProductView
from renderer.models import RenderJob
from renderer.tasks import process_render_job
from .serializers import (
    ProductSerializer, 
    ProductViewSerializer, 
    RenderJobSerializer, 
    RenderJobStatusSerializer
)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer

class ProductViewListView(generics.ListAPIView):
    serializer_class = ProductViewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductView.objects.filter(product_id=product_id)

class RenderJobCreateView(generics.CreateAPIView):
    queryset = RenderJob.objects.all()
    serializer_class = RenderJobSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        job = serializer.save()
        # Trigger Celery task
        process_render_job.delay(job.id)

class LandingView(TemplateView):
    template_name = 'landing.html'

class HomeView(TemplateView):
    template_name = 'home.html'

class RenderJobStatusView(generics.RetrieveAPIView):
    queryset = RenderJob.objects.all()
    serializer_class = RenderJobStatusSerializer
    lookup_field = 'id'
