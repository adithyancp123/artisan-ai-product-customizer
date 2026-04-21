import cv2
import numpy as np
from PIL import Image
import io
from django.core.files.base import ContentFile

def render_design(base_image_path, design_image_path, x, y, width, height):
    """
    Renders a design onto a base image at specified coordinates and dimensions.
    Uses PIL for high-quality alpha compositing and NumPy/OpenCV for any 
    pixel-level realistic blending.
    """
    # Load images
    base = Image.open(base_image_path).convert("RGBA")
    design = Image.open(design_image_path).convert("RGBA")

    # Resize design to fit the specified print area
    design = design.resize((width, height), Image.Resampling.LANCZOS)

    # Create a transparent overlay of the same size as the base
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    overlay.paste(design, (x, y), design)

    # Composite the images
    # For a more realistic look, we could use OpenCV to apply displacement maps 
    # or multiply blending based on shadows in the base image.
    # Here we perform a standard high-quality alpha composite.
    combined = Image.alpha_composite(base, overlay)

    # Convert back to RGB for final output (or keep RGBA if needed)
    final_image = combined.convert("RGB")

    # Save to a bytes buffer
    buffer = io.BytesIO()
    final_image.save(buffer, format="JPEG", quality=95)
    
    return buffer.getvalue()
