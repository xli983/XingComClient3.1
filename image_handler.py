

def set_image_value(value):
    global image  # Indicate that we want to modify the global variable
    image = value

# Function to access and use the global variable 'image'
def access_image():
    if image is not None:
       return image
    else:
        print("Image is not set.")
