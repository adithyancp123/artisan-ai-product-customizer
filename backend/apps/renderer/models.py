from django.db import models
from products.models import Product, ProductView

class RenderJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    uploaded_design = models.ImageField(upload_to='uploads/designs/')
    selected_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_view = models.ForeignKey(ProductView, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0)  # 0 to 100
    output_image = models.ImageField(upload_to='renders/', null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job #{self.id} - {self.status}"
