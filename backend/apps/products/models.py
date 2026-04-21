from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductView(models.Model):
    ANGLE_CHOICES = [
        ('front', 'Front'),
        ('back', 'Back'),
        ('side', 'Side'),
    ]
    
    product = models.ForeignKey(Product, related_name='views', on_delete=models.CASCADE)
    angle_type = models.CharField(max_length=10, choices=ANGLE_CHOICES)
    base_image = models.ImageField(upload_to='base_products/')
    
    # Print area coordinates and dimensions (normalized or pixels, here we use pixels)
    print_x = models.IntegerField(default=0, help_text="X coordinate of print area")
    print_y = models.IntegerField(default=0, help_text="Y coordinate of print area")
    print_width = models.IntegerField(default=200, help_text="Width of print area")
    print_height = models.IntegerField(default=200, help_text="Height of print area")

    def __str__(self):
        return f"{self.product.name} - {self.get_angle_type_display()}"
