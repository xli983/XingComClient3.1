from PIL import Image

def preprocess_image(image_path):
    image = image_path.convert("RGBA")
    pixels = image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b, a = pixels[i, j]
            new_r = int(r + (255 - r) * (1 - a / 255))
            new_g = int(g + (255 - g) * (1 - a / 255))
            new_b = int(b + (255 - b) * (1 - a / 255))
            pixels[i, j] = (new_r, new_g, new_b, 255)

    return image.convert("RGB")


def postprocess_image(rgb_image_path):
    rgb_image = rgb_image_path.convert("RGB")
    pixels = rgb_image.load()

    new_image = Image.new("RGBA", rgb_image.size)
    new_pixels = new_image.load()

    for i in range(rgb_image.size[0]):
        for j in range(rgb_image.size[1]):
            r, g, b = pixels[i, j]
            alpha = int(255 - (r + g + b) / 3)
            new_pixels[i, j] = (0, 0, 0, alpha)

    return new_image