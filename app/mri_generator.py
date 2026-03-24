"""
MRI Image Generation for Demo
Creates synthetic MRI-like images for demonstration purposes
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import io
import base64

def generate_synthetic_brain_mri(size=256, quality='low'):
    """
    Generate a synthetic brain MRI image for demonstration
    
    Args:
        size: Image dimension (square)
        quality: 'low', 'medium', or 'high'
    
    Returns:
        PIL Image object
    """
    # Create base brain structure
    img = Image.new('L', (size, size), color=0)
    draw = ImageDraw.Draw(img)
    
    # Draw brain outline (ellipse)
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], fill=100, outline=150)
    
    # Add brain structures
    # Ventricles (darker regions in center)
    center = size // 2
    ventricle_size = size // 6
    draw.ellipse([center - ventricle_size//2, center - ventricle_size//3,
                  center + ventricle_size//2, center + ventricle_size//3],
                 fill=30, outline=40)
    
    # Gray matter vs white matter (subtle variations)
    for _ in range(20):
        x = np.random.randint(margin + 20, size - margin - 20)
        y = np.random.randint(margin + 20, size - margin - 20)
        r = np.random.randint(10, 30)
        intensity = np.random.randint(80, 120)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=intensity)
    
    # Add some anatomical features
    # Corpus callosum (bright band in center)
    draw.rectangle([center - 40, center - 5, center + 40, center + 5],
                   fill=140)
    
    # Apply quality-specific degradation
    if quality == 'low':
        # Simulate low-field MRI: lower SNR, artifacts
        img_array = np.array(img, dtype=np.float32)
        
        # Add noise
        noise = np.random.normal(0, 25, img_array.shape)
        img_array += noise
        
        # Add ringing artifacts
        img_array = img_array * (1 + 0.1 * np.sin(np.linspace(0, 4*np.pi, size))[:, np.newaxis])
        
        # Reduce resolution
        img = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Add aliasing
        img_array = np.array(img)
        img_array[::4, :] = img_array[::4, :] * 0.7
        img = Image.fromarray(img_array.astype(np.uint8))
        
    elif quality == 'medium':
        # U-Net enhanced: reduced noise, some artifacts remain
        img_array = np.array(img, dtype=np.float32)
        noise = np.random.normal(0, 10, img_array.shape)
        img_array += noise
        img = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
    elif quality == 'high':
        # VarNet or ground truth: clean, high quality
        img = img.filter(ImageFilter.SMOOTH)
    
    return img

def create_comparison_image(low, medium, high, ground_truth):
    """Create a 4-panel comparison image"""
    width, height = low.size
    comparison = Image.new('L', (width * 4, height), color=0)
    
    comparison.paste(low, (0, 0))
    comparison.paste(medium, (width, 0))
    comparison.paste(high, (width * 2, 0))
    comparison.paste(ground_truth, (width * 3, 0))
    
    return comparison

def image_to_base64(img):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def generate_mri_example_set():
    """Generate a complete set of MRI examples for the demo"""
    examples = {}
    
    # Case 1: Normal brain scan
    examples['normal'] = {
        'name': 'Normal Brain Scan',
        'description': 'Healthy adult brain, age 35',
        'low': generate_synthetic_brain_mri(256, 'low'),
        'unet': generate_synthetic_brain_mri(256, 'medium'),
        'varnet': generate_synthetic_brain_mri(256, 'high'),
        'ground_truth': generate_synthetic_brain_mri(256, 'high')
    }
    
    return examples

def calculate_quality_metrics(enhanced, ground_truth):
    """
    Calculate PSNR and SSIM-like metrics
    (Simplified for demo purposes)
    """
    enhanced_array = np.array(enhanced, dtype=np.float32)
    gt_array = np.array(ground_truth, dtype=np.float32)
    
    # PSNR calculation
    mse = np.mean((enhanced_array - gt_array) ** 2)
    if mse == 0:
        psnr = 100
    else:
        psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    
    # Simplified SSIM (correlation-based)
    enhanced_norm = (enhanced_array - enhanced_array.mean()) / (enhanced_array.std() + 1e-8)
    gt_norm = (gt_array - gt_array.mean()) / (gt_array.std() + 1e-8)
    ssim = np.mean(enhanced_norm * gt_norm)
    ssim = (ssim + 1) / 2  # Normalize to [0, 1]
    
    return {
        'PSNR': f"{psnr:.2f} dB",
        'SSIM': f"{ssim:.3f}",
        'Quality': 'Excellent' if ssim > 0.9 else 'Good' if ssim > 0.8 else 'Fair'
    }

if __name__ == "__main__":
    # Test image generation
    print("Generating synthetic MRI images...")
    
    low = generate_synthetic_brain_mri(256, 'low')
    medium = generate_synthetic_brain_mri(256, 'medium')
    high = generate_synthetic_brain_mri(256, 'high')
    gt = generate_synthetic_brain_mri(256, 'high')
    
    low.save('/home/claude/test_low.png')
    medium.save('/home/claude/test_medium.png')
    high.save('/home/claude/test_high.png')
    gt.save('/home/claude/test_gt.png')
    
    print("✅ Images generated successfully!")
    print("   - test_low.png (Low-field MRI)")
    print("   - test_medium.png (U-Net Enhanced)")
    print("   - test_high.png (VarNet Enhanced)")
    print("   - test_gt.png (Ground Truth)")
    
    # Calculate metrics
    metrics_unet = calculate_quality_metrics(medium, gt)
    metrics_varnet = calculate_quality_metrics(high, gt)
    
    print(f"\n📊 Quality Metrics:")
    print(f"U-Net: PSNR={metrics_unet['PSNR']}, SSIM={metrics_unet['SSIM']}")
    print(f"VarNet: PSNR={metrics_varnet['PSNR']}, SSIM={metrics_varnet['SSIM']}")
