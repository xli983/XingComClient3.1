from PIL import Image, ImageEnhance
import numpy as np

def process_image(image_path, enhance_contrast=True, black_threshold=50):
    # Load the image
    img = image_path
        # Optionally enhance contrast
    if enhance_contrast:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(10.0)  # Increase contrast; adjust the factor as needed

        # Convert to NumPy array for pixel manipulation
        data = np.array(img)

        # Set pixels with R, G, and B values above the threshold to transparent
        # Only very dark (black) pixels will be retained
        red, green, blue, alpha = data.T
        non_black_areas = (red > black_threshold) | (blue > black_threshold) | (green > black_threshold)
        data[..., :-1][non_black_areas.T] = (0, 0, 0)  # Set color to black (optional)
        data[..., -1][non_black_areas.T] = 0          # Set alpha to 0 (transparent)

        # Convert back to Image and save
        result_image = Image.fromarray(data)
        return result_image
