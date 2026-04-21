from django.urls import path
from .views import (
    ProductListView, 
    ProductViewListView, 
    RenderJobCreateView, 
    RenderJobStatusView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:product_id>/views/', ProductViewListView.as_view(), name='product-view-list'),
    path('render-preview/', RenderJobCreateView.as_view(), name='render-preview'),
    path('job/<int:id>/status/', RenderJobStatusView.as_view(), name='job-status'),
]
