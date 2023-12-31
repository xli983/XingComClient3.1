import json_modes
import random

import multiprocessing as mp
from multiprocessing.managers import BaseManager
from multiprocessing import Manager, Process, Value
from multiprocessing import Pool, Queue, cpu_count

from PIL import Image, ImageFile
import numpy as np
import io
from io import BytesIO
import os
# import os
# from typing import Tuple


def image_to_uint8(image_path):
    img = image_path
    img = img.convert("RGBA")
    image_array = np.array(img, dtype='uint8')
    mask_array = np.zeros_like(image_array)
    mask_array[:,:,-1] = 225
    return {'image': image_array, 'mask': mask_array}

def getKey(dict, key):
    if key in dict:
        return dict[key]
    else:
        return None
def decodePNG(pngBytestring):
    # assuming `png_bytestring` contains the PNG image data
    image_data = io.BytesIO(pngBytestring)
    image = Image.open(image_data)
    return image 
    
def image_to_png_bytestring(image):
    png_bytestring = BytesIO()
    image.save(png_bytestring, format="PNG")
    png_bytestring.seek(0)
    return png_bytestring.getvalue()

def add_lora(self, input_lora):
    base_model_clip = 4  # Starting model and clip value
    current_id = 22  # Starting ID
    for lora_entry in input_lora:
        lora_name = lora_entry['name']
        intensity = lora_entry['intensity']
        lora_item = {
            "inputs": {
                "lora_name": f"{lora_name}.safetensors",
                "strength_model": intensity,
                "strength_clip": 1.0,
                "model": [str(base_model_clip), 0],
                "clip": [str(base_model_clip), 1]
            },
            "class_type": "LoraLoader"
        }
        self.data[str(current_id)] = lora_item  # Use self.data for item assignment
        # Update values for the next iteration
        base_model_clip = current_id
        current_id += 1
