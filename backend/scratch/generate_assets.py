import os
from PIL import Image, ImageDraw

def create_placeholder(filename, color):
    path = os.path.join('media', 'products', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Create a 1000x1000 image with a solid color
    img = Image.new('RGB', (1000, 1000), color)
    draw = ImageDraw.Draw(img)
    
    # Draw a very basic T-shirt outline
    # Front
    draw.polygon([(200, 200), (800, 200), (800, 900), (200, 900)], fill=(240, 240, 240))
    # Sleeves
    draw.polygon([(200, 200), (50, 400), (200, 500)], fill=(240, 240, 240))
    draw.polygon([(800, 200), (950, 400), (800, 500)], fill=(240, 240, 240))
    
    img.save(path)
    print(f"Created: {path}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    create_placeholder('white_tshirt_front.png', (255, 255, 255))
    create_placeholder('white_tshirt_side.png', (245, 245, 245))
    create_placeholder('white_tshirt_back.png', (240, 240, 240))
