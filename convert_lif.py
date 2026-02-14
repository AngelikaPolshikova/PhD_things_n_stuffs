from tifffile import imread, imwrite
import numpy as np
import os
from pathlib import Path

# Set your directories
input_dir = Path(r'/mnt/c/Users/aplosh/Desktop/to_convert')
output_dir = Path(r'/mnt/c/Users/aplosh/Desktop/to_convert/converted')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get all TIFF files
tiff_files = list(input_dir.glob("*.tif")) + list(input_dir.glob("*.tiff"))

print(f"Found {len(tiff_files)} TIFF files")

# Convert each file
for tiff_file in tiff_files:
    try:
        print(f"\nConverting {tiff_file.name}...")
        
        # Read the image
        img = imread(tiff_file)
        
        # Print original shape
        print(f"  Original shape: {img.shape}, dtype: {img.dtype}")
        
        # Reshape from (C, Z, Y, X) to (T, Z, C, Y, X) - adding T dimension     commented out to convert 3D thingy
        # ImageJ wants TZCYX order
        # img_reshaped = img[np.newaxis, :, :, :, :]  # Add T dimension at front
        # img_reshaped = np.transpose(img_reshaped, (0, 2, 1, 3, 4))  # Rearrange to TZCYX


        img_reshaped = img[np.newaxis, :, np.newaxis, :, :]
        
        print(f"  Reshaped to: {img_reshaped.shape}")
        
        # Save as uncompressed TIFF
        output_path = output_dir / tiff_file.name
        imwrite(
            output_path, 
            img_reshaped, 
            compression=None, 
            imagej=True
        )
        
        print(f"  ✓ Saved to {output_path}")
        
    except Exception as e:
        print(f"  ✗ Error with {tiff_file.name}: {e}")

print("\nConversion complete!")