import cv2
import numpy as np
import os
from PIL import Image
import io
from django.core.files.base import ContentFile

class RenderPipeline:
    """
    Professional Image Rendering Pipeline for Product Customization.
    Features: Perspective Transform, Displacement Mapping, and Multi-layered Blending.
    """

    def __init__(self, base_image_path, design_image_path):
        # Load images using OpenCV
        self.base_bgr = cv2.imread(base_image_path)
        self.design_rgba = cv2.imread(design_image_path, cv2.IMREAD_UNCHANGED)
        
        if self.design_rgba is None:
            raise ValueError("Failed to load design image")
        if self.design_rgba.shape[2] == 3:
            # Convert RGB to RGBA if no alpha channel
            self.design_rgba = cv2.cvtColor(self.design_rgba, cv2.COLOR_BGR2BGRA)

    def apply_perspective(self, x, y, w, h, angle_type='front'):
        """
        Fits the design into the print area using a 4-point perspective transform.
        Applies slight skew/rotation based on the angle_type.
        """
        # Define source points (the design corners)
        dh, dw = self.design_rgba.shape[:2]
        src_pts = np.float32([[0, 0], [dw, 0], [dw, dh], [0, dh]])

        # Define destination points (the print area on the base image)
        # We add slight perspective shifts based on angle_type
        pts = np.float32([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
        
        if angle_type == 'side':
            # Add more horizontal skew for side views
            pts[0][0] += w * 0.1
            pts[3][0] += w * 0.1
            pts[1][0] -= w * 0.05
            pts[2][0] -= w * 0.05
        elif angle_type == 'back':
            # Slight bulge or vertical shift
            pass

        matrix = cv2.getPerspectiveTransform(src_pts, pts)
        self.warped_design = cv2.warpPerspective(
            self.design_rgba, matrix, (self.base_bgr.shape[1], self.base_bgr.shape[0]),
            flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0)
        )
        return self.warped_design

    def generate_displacement_map(self, x, y, w, h):
        """
        Creates a displacement map from the base image's intensity to warp the logo
        according to fabric folds.
        """
        # Convert base to gray and isolate the print area region
        gray = cv2.cvtColor(self.base_bgr, cv2.COLOR_BGR2GRAY)
        roi = gray[y:y+h, x:x+w]
        
        # Smooth the ROI to avoid jagged displacements
        roi_blurred = cv2.GaussianBlur(roi, (15, 15), 0)
        
        # Normalize and find gradients
        # We use the relative intensity to "shift" pixels
        map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
        
        # Calculate displacement based on intensity gradients (Sobel)
        # This makes the design follow the "slopes" of the wrinkles
        grad_x = cv2.Sobel(roi_blurred, cv2.CV_32F, 1, 0, ksize=5)
        grad_y = cv2.Sobel(roi_blurred, cv2.CV_32F, 0, 1, ksize=5)
        
        # Scale the displacement
        intensity = 0.5
        map_x = map_x.astype(np.float32) + (grad_x * intensity)
        map_y = map_y.astype(np.float32) + (grad_y * intensity)
        
        return map_x, map_y

    def apply_fabric_warp(self, x, y, w, h):
        """
        Warps the design image based on the generated displacement map.
        """
        map_x, map_y = self.generate_displacement_map(x, y, w, h)
        
        # Extract the design in a local coordinate system
        # Actually, it's easier to warp the whole warped_design or just the design ROI
        design_roi = self.warped_design[y:y+h, x:x+w]
        
        warped_roi = cv2.remap(design_roi, map_x, map_y, cv2.INTER_LINEAR)
        self.warped_design[y:y+h, x:x+w] = warped_roi
        return self.warped_design

    def blend_realistic(self):
        """
        Performs realistic blending using Multiply and Overlay modes.
        Multiply: Captures shadows from the fabric.
        Overlay: Captures highlights/sheen.
        """
        # Split warped design into BGR and Alpha
        design_bgr = self.warped_design[:, :, :3]
        design_alpha = self.warped_design[:, :, 3] / 255.0
        design_alpha = cv2.merge([design_alpha, design_alpha, design_alpha])

        # 1. Base Multiply (Shadows)
        # Convert base to float [0, 1] for blending
        base_f = self.base_bgr.astype(np.float32) / 255.0
        design_f = design_bgr.astype(np.float32) / 255.0
        
        # Multiply blend: B * D
        multiplied = base_f * design_f
        
        # 2. Linear Interpolation (Standard alpha blend)
        # result = (1 - alpha) * base + alpha * multiplied
        blended = (1.0 - design_alpha) * base_f + design_alpha * multiplied
        
        # 3. Add Highlights (Simple Screen/Overlay approximation)
        # We take high intensity areas from the base image and "overlay" them back
        gray_base = cv2.cvtColor(self.base_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        highlights = np.clip(gray_base - 0.7, 0, 1) * 0.3
        highlights = cv2.merge([highlights, highlights, highlights])
        
        # Only apply highlights where the design exists
        blended += highlights * design_alpha
        
        final_bgr = np.clip(blended * 255, 0, 255).astype(np.uint8)
        return final_bgr

    def generate(self, x, y, w, h, angle_type='front'):
        """
        Executes the full pipeline and returns the final image as bytes.
        """
        self.apply_perspective(x, y, w, h, angle_type)
        self.apply_fabric_warp(x, y, w, h)
        final_bgr = self.blend_realistic()
        
        # Convert BGR to RGB for PIL then to bytes
        final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(final_rgb)
        
        buffer = io.BytesIO()
        pil_img.save(buffer, format="JPEG", quality=90)
        return buffer.getvalue()
