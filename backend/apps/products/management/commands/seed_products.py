import os
import random
import io
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw

from products.models import Product, ProductView

class Command(BaseCommand):
    help = 'Seed database with sample apparel products and high-quality generated assets'

    def handle(self, *args, **options):
        self.stdout.write('Seeding products...')
        
        # Ensure media directory exists
        media_path = os.path.join('media', 'base_products')
        os.makedirs(media_path, exist_ok=True)

        # Helper to generate a placeholder image
        def get_placeholder(name, color):
            # Create a 1000x1000 image with a solid color representing a shirt
            img = Image.new('RGB', (1000, 1000), (30, 30, 30)) # Dark background
            draw = ImageDraw.Draw(img)
            
            # Draw shirt body
            draw.polygon([(250,200), (750,200), (750,900), (250,900)], fill=color)
            # Sleeves
            draw.polygon([(250,200), (100,350), (250,450)], fill=color)
            draw.polygon([(750,200), (900,350), (750,450)], fill=color)
            
            # Save to bytes
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            return ContentFile(buf.getvalue(), name=name)

        products = [
            {
                'name': 'Premium Cotton T-Shirt',
                'views': [
                    {'type': 'front', 'color': (255, 255, 255), 'x': 250, 'y': 350, 'w': 500, 'h': 350},
                    {'type': 'back', 'color': (255, 255, 255), 'x': 250, 'y': 350, 'w': 500, 'h': 350},
                    {'type': 'side', 'color': (255, 255, 255), 'x': 450, 'y': 300, 'w': 100, 'h': 300},
                ]
            },
            {
                'name': 'Urban Hoodie',
                'views': [
                    {'type': 'front', 'color': (60, 60, 60), 'x': 300, 'y': 300, 'w': 400, 'h': 450},
                    {'type': 'back', 'color': (60, 60, 60), 'x': 300, 'y': 300, 'w': 400, 'h': 450},
                ]
            }
        ]

        for p_data in products:
            product, created = Product.objects.update_or_create(
                name=p_data['name'],
                defaults={'active': True}
            )
            
            for v_data in p_data['views']:
                filename = f"{product.name.lower().replace(' ', '_')}_{v_data['type']}.png"
                view, v_created = ProductView.objects.update_or_create(
                    product=product,
                    angle_type=v_data['type'],
                    defaults={
                        'print_x': v_data['x'],
                        'print_y': v_data['y'],
                        'print_width': v_data['w'],
                        'print_height': v_data['h'],
                    }
                )
                
                # Force save new image to ensure we have the high-quality assets
                view.base_image.save(filename, get_placeholder(filename, v_data['color']))
                
                self.stdout.write(f"  - {product.name} ({v_data['type']})")

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with smart assets.'))
