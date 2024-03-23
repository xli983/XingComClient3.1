test ={
    '3': {
        'inputs': {
            'seed': 863048463356742,
            'steps': 20,
            'cfg': 8.0,
            'sampler_name': 'dpmpp_2m',
            'scheduler': 'normal',
            'denoise': 0.8533325195312503,
            'model': ['4', 0],
            'positive': ['6', 0],
            'negative': ['7', 0],
            'latent_image': ['17', 0]
        },
        'class_type': 'KSampler'
    },

    '4': {
        'inputs': {
            'ckpt_name': 'etherBluMix_etherBluMix5.safetensors'
        },
        'class_type': 'CheckpointLoaderSimple'
    },

    '6': {
        'inputs': {
            'text': '',
            'clip': ['4', 1]
        },
        'class_type': 'CLIPTextEncode'
    },

    '7': {
        'inputs': {
            'text': 'text, watermark, easynegative',
            'clip': ['4', 1]
        },
        'class_type': 'CLIPTextEncode'
    },

    '8': {
        'inputs': {
            'samples': ['3', 0],
            'vae': ['12', 0]
        },
        'class_type': 'VAEDecode'
    },

    '9': {
        'inputs': {
            'filename_prefix': 'ComfyUI',
            'images': ['8', 0]
        },
        'class_type': 'SaveImage'
    },

    '10': {
        'inputs': {
            'image': '00018-2010144025.png',
            'choose file to upload': 'image'
        },
        'class_type': 'LoadImage'
    },

    '12': {
        'inputs': {
            'vae_name': 'kl-f8-anime2.vae.pt'
        },
        'class_type': 'VAELoader'
    },

    '13': {
        'inputs': {
            'pixels': ['10', 0],
            'vae': ['12', 0]
        },
        'class_type': 'VAEEncode'
    },

    '17': {
        'inputs': {
            'upscale_method': 'nearest-exact',
            'width': 1080,
            'height': 736,
            'crop': 'disabled',
            'samples': ['13', 0]
        },
        'class_type': 'LatentUpscale'
    }
}

test_extra_data = {'extra_pnginfo': {'workflow': {'last_node_id': 21, 'last_link_id': 30, 'nodes': [{'id': 12, 'type': 'VAELoader', 'pos': [17, 737], 'size': {'0': 315, '1': 58}, 'flags': {}, 'order': 0, 'mode': 0, 'outputs': [{'name': 'VAE', 'type': 'VAE', 'links': [13, 16], 'shape': 3, 'slot_index': 0}], 'properties': {'Node name for S&R': 'VAELoader'}, 'widgets_values': ['kl-f8-anime2.vae.pt']}, {'id': 7, 'type': 'CLIPTextEncode', 'pos': [422, 394], 'size': {'0': 425.27801513671875, '1': 180.6060791015625}, 'flags': {}, 'order': 5, 'mode': 0, 'inputs': [{'name': 'clip', 'type': 'CLIP', 'link': 5}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [6], 'slot_index': 0}], 'properties': {'Node name for S&R': 'CLIPTextEncode'}, 'widgets_values': ['text, watermark, easynegative']}, {'id': 13, 'type': 'VAEEncode', 'pos': [443, 612], 'size': {'0': 210, '1': 46}, 'flags': {}, 'order': 4, 'mode': 0, 'inputs': [{'name': 'pixels', 'type': 'IMAGE', 'link': 14}, {'name': 'vae', 'type': 'VAE', 'link': 16}], 'outputs': [{'name': 'LATENT', 'type': 'LATENT', 'links': [21], 'shape': 3, 'slot_index': 0}], 'properties': {'Node name for S&R': 'VAEEncode'}}, {'id': 3, 'type': 'KSampler', 'pos': [1049, 124], 'size': {'0': 315, '1': 262}, 'flags': {}, 'order': 8, 'mode': 0, 'inputs': [{'name': 'model', 'type': 'MODEL', 'link': 27}, {'name': 'positive', 'type': 'CONDITIONING', 'link': 4}, {'name': 'negative', 'type': 'CONDITIONING', 'link': 6}, {'name': 'latent_image', 'type': 'LATENT', 'link': 22, 'slot_index': 3}], 'outputs': [{'name': 'LATENT', 'type': 'LATENT', 'links': [7], 'slot_index': 0}], 'properties': {'Node name for S&R': 'KSampler'}, 'widgets_values': [930840557640585, 'randomize', 20, 8, 'dpmpp_2m', 'normal', 0.8533325195312503]}, {'id': 17, 'type': 'LatentUpscale', 'pos': [667, 614], 'size': {'0': 315, '1': 130}, 'flags': {}, 'order': 7, 'mode': 0, 'inputs': [{'name': 'samples', 'type': 'LATENT', 'link': 21}], 'outputs': [{'name': 'LATENT', 'type': 'LATENT', 'links': [22], 'shape': 3, 'slot_index': 0}], 'properties': {'Node name for S&R': 'LatentUpscale'}, 'widgets_values': ['nearest-exact', 1080, 736, 'disabled']}, {'id': 18, 'type': 'ImageUpscaleWithModel', 'pos': [1585, 451], 'size': {'0': 241.79998779296875, '1': 46}, 'flags': {}, 'order': 1, 'mode': 0, 'inputs': [{'name': 'upscale_model', 'type': 'UPSCALE_MODEL', 'link': None}, {'name': 'image', 'type': 'IMAGE', 'link': None}], 'outputs': [{'name': 'IMAGE', 'type': 'IMAGE', 'links': None, 'shape': 3}], 'properties': {'Node name for S&R': 'ImageUpscaleWithModel'}}, {'id': 10, 'type': 'LoadImage', 'pos': [18, 354], 'size': {'0': 315, '1': 314}, 'flags': {}, 'order': 2, 'mode': 0, 'outputs': [{'name': 'IMAGE', 'type': 'IMAGE', 'links': [14], 'shape': 3, 'slot_index': 0}, {'name': 'MASK', 'type': 'MASK', 'links': [], 'shape': 3, 'slot_index': 1}], 'properties': {'Node name for S&R': 'LoadImage'}, 'widgets_values': ['00018-2010144025.png', 'image']}, {'id': 4, 'type': 'CheckpointLoaderSimple', 'pos': [34, 127], 'size': {'0': 315, '1': 98}, 'flags': {}, 'order': 3, 'mode': 0, 'outputs': [{'name': 'MODEL', 'type': 'MODEL', 'links': [27], 'slot_index': 0}, {'name': 'CLIP', 'type': 'CLIP', 'links': [5, 29], 'slot_index': 1}, {'name': 'VAE', 'type': 'VAE', 'links': [], 'slot_index': 2}], 'properties': {'Node name for S&R': 'CheckpointLoaderSimple'}, 'widgets_values': ['etherBluMix_etherBluMix5.safetensors']}, {'id': 6, 'type': 'CLIPTextEncode', 'pos': [421, 189], 'size': {'0': 422.84503173828125, '1': 164.31304931640625}, 'flags': {}, 'order': 6, 'mode': 0, 'inputs': [{'name': 'clip', 'type': 'CLIP', 'link': 29}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [4], 'slot_index': 0}], 'properties': {'Node name for S&R': 'CLIPTextEncode'}, 'widgets_values': ['cat ear girl, big cat ears']}, {'id': 8, 'type': 'VAEDecode', 'pos': [1400, 632], 'size': {'0': 210, '1': 46}, 'flags': {}, 'order': 9, 'mode': 0, 'inputs': [{'name': 'samples', 'type': 'LATENT', 'link': 7}, {'name': 'vae', 'type': 'VAE', 'link': 13, 'slot_index': 1}], 'outputs': [{'name': 'IMAGE', 'type': 'IMAGE', 'links': [9], 'slot_index': 0}], 'properties': {'Node name for S&R': 'VAEDecode'}}, {'id': 9, 'type': 'SaveImage', 'pos': [1647, 625], 'size': {'0': 210, '1': 270}, 'flags': {}, 'order': 10, 'mode': 0, 'inputs': [{'name': 'images', 'type': 'IMAGE', 'link': 9}], 'properties': {}, 'widgets_values': ['ComfyUI']}], 'links': [[4, 6, 0, 3, 1, 'CONDITIONING'], [5, 4, 1, 7, 0, 'CLIP'], [6, 7, 0, 3, 2, 'CONDITIONING'], [7, 3, 0, 8, 0, 'LATENT'], [9, 8, 0, 9, 0, 'IMAGE'], [13, 12, 0, 8, 1, 'VAE'], [14, 10, 0, 13, 0, 'IMAGE'], [16, 12, 0, 13, 1, 'VAE'], [21, 13, 0, 17, 0, 'LATENT'], [22, 17, 0, 3, 3, 'LATENT'], [27, 4, 0, 3, 0, 'MODEL'], [29, 4, 1, 6, 0, 'CLIP']], 'groups': [], 'config': {}, 'extra': {}, 'version': 0.4}}, 'client_id': '5ac85150dffb433f9bd98e4c35ed700f'}
test_execute_outputs = ['9']

fast = {'1': {'inputs': {'image': '6e9f1902652632b8c29dc5daa21912f (1).png', 'upload': 'image'}, 'class_type': 'LoadImage'}, '2': {'inputs': {'upscale_method': 'nearest-exact', 'width': 1080, 'height': 736, 'crop': 'disabled', 'image': ['1', 0]}, 'class_type': 'ImageScale'}, '3': {'inputs': {'seed': 431316963001212, 'steps': 6, 'cfg': 1.5, 'sampler_name': 'lcm', 'scheduler': 'sgm_uniform', 'denoise': 0.5, 'preview_method': 'auto', 'vae_decode': 'true', 'model': ['6', 0], 'positive': ['8', 0], 'negative': ['9', 0], 'latent_image': ['7', 0], 'optional_vae': ['4', 0]}, 'class_type': 'KSampler (Efficient)'}, '4': {'inputs': {'vae_name': 'kl-f8-anime2.vae.pt'}, 'class_type': 'VAELoader'}, '5': {'inputs': {'ckpt_name': 'etherBluMix_etherBluMix5.safetensors'}, 'class_type': 'CheckpointLoaderSimple'}, '6': {'inputs': {'lora_name': 'pytorch_lora_weights.safetensors', 'strength_model': 1.0, 'strength_clip': 1.0, 'model': ['5', 0], 'clip': ['5', 1]}, 'class_type': 'LoraLoader'}, '7': {'inputs': {'pixels': ['2', 0], 'vae': ['4', 0]}, 'class_type': 'VAEEncode'}, '8': {'inputs': {'text': '', 'clip': ['6', 1]}, 'class_type': 'CLIPTextEncode'}, '9': {'inputs': {'text': '', 'clip': ['6', 1]}, 'class_type': 'CLIPTextEncode'}, '10': {'inputs': {'filename_prefix': 'ComfyUI', 'images': ['3', 5]}, 'class_type': 'SaveImage'}}
fast_extra_data = {}
fast_execute_outputs = ['10']


upscale = {
    '6': {
        'inputs': {
            'text': ' ',
            'clip': ['17', 1]
        },
        'class_type': 'CLIPTextEncode'
    },
    '11': {
        'inputs': {
            'image': '1067522a01f49e74d10359e42025fb9 (3).png',
            'choose file to upload': 'image'
        },
        'class_type': 'LoadImage'
    },
    '12': {
        'inputs': {
            'strength': 1.0,
            'conditioning': ['6', 0],
            'control_net': ['13', 0],
            'image': ['11', 0]
        },
        'class_type': 'ControlNetApply'
    },
    '13': {
        'inputs': {
            'control_net_name': 'control_v11f1e_sd15_tile.pth'
        },
        'class_type': 'ControlNetLoader'
    },
    '15': {
        'inputs': {
            'upscale_by': 4.0,
            'seed': 1032110734710495,
            'steps': 20,
            'cfg': 8.0,
            'sampler_name': 'euler',
            'scheduler': 'normal',
            'denoise': 0.4,
            'mode_type': 'Linear',
            'tile_width': 512,
            'tile_height': 512,
            'mask_blur': 8,
            'tile_padding': 32,
            'seam_fix_mode': 'None',
            'seam_fix_denoise': 1.0,
            'seam_fix_width': 64,
            'seam_fix_mask_blur': 8,
            'seam_fix_padding': 16,
            'force_uniform_tiles': 'enable',
            'image': ['11', 0],
            'model': ['17', 0],
            'positive': ['12', 0],
            'negative': ['16', 0],
            'vae': ['18', 0],
            'upscale_model': ['19', 0]
        },
        'class_type': 'UltimateSDUpscale'
    },
    '16': {
        'inputs': {
            'text': '',
            'clip': ['17', 1]
        },
        'class_type': 'CLIPTextEncode'
    },
    '17': {
        'inputs': {
            'ckpt_name': 'etherBluMix_etherBluMix5.safetensors'
        },
        'class_type': 'CheckpointLoaderSimple'
    },
    '18': {
        'inputs': {
            'vae_name': 'kl-f8-anime2.vae.pt'
        },
        'class_type': 'VAELoader'
    },
    '19': {
        'inputs': {
            'model_name': 'RealESRGAN_x4plus_anime_6B.pth'
        },
        'class_type': 'UpscaleModelLoader'
    },
    '20': {
        'inputs': {
            'filename_prefix': 'ComfyUI',
            'images': ['15', 0]
        },
        'class_type': 'SaveImage'
    }
}
upscale_extra_data = {'extra_pnginfo': {'workflow': {'last_node_id': 20, 'last_link_id': 27, 'nodes': [{'id': 12, 'type': 'ControlNetApply', 'pos': [556, -468], 'size': {'0': 317.4000244140625, '1': 98}, 'flags': {}, 'order': 7, 'mode': 0, 'inputs': [{'name': 'conditioning', 'type': 'CONDITIONING', 'link': 18}, {'name': 'control_net', 'type': 'CONTROL_NET', 'link': 16, 'slot_index': 1}, {'name': 'image', 'type': 'IMAGE', 'link': 15}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [19], 'shape': 3, 'slot_index': 0}], 'properties': {'Node name for S&R': 'ControlNetApply'}, 'widgets_values': [1]}, {'id': 6, 'type': 'CLIPTextEncode', 'pos': [213, -602], 'size': {'0': 210, '1': 76}, 'flags': {}, 'order': 6, 'mode': 0, 'inputs': [{'name': 'clip', 'type': 'CLIP', 'link': 23}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [18], 'slot_index': 0}], 'properties': {'Node name for S&R': 'CLIPTextEncode'}, 'widgets_values': [' ']}, {'id': 16, 'type': 'CLIPTextEncode', 'pos': [209, -481], 'size': {'0': 210, '1': 76.00000762939453}, 'flags': {}, 'order': 5, 'mode': 0, 'inputs': [{'name': 'clip', 'type': 'CLIP', 'link': 22}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [20], 'shape': 3, 'slot_index': 0}], 'properties': {'Node name for S&R': 'CLIPTextEncode'}, 'widgets_values': ['']}, {'id': 13, 'type': 'ControlNetLoader', 'pos': [150, -352], 'size': {'0': 315, '1': 58}, 'flags': {}, 'order': 0, 'mode': 0, 'outputs': [{'name': 'CONTROL_NET', 'type': 'CONTROL_NET', 'links': [16], 'shape': 3}], 'properties': {'Node name for S&R': 'ControlNetLoader'}, 'widgets_values': ['control_v11f1e_sd15_tile.pth']}, {'id': 17, 'type': 'CheckpointLoaderSimple', 'pos': [555, -643], 'size': {'0': 315, '1': 98}, 'flags': {}, 'order': 1, 'mode': 0, 'outputs': [{'name': 'MODEL', 'type': 'MODEL', 'links': [21], 'shape': 3, 'slot_index': 0}, {'name': 'CLIP', 'type': 'CLIP', 'links': [22, 23], 'shape': 3, 'slot_index': 1}, {'name': 'VAE', 'type': 'VAE', 'links': None, 'shape': 3}], 'properties': {'Node name for S&R': 'CheckpointLoaderSimple'}, 'widgets_values': ['etherBluMix_etherBluMix5.safetensors']}, {'id': 18, 'type': 'VAELoader', 'pos': [666, -317], 'size': {'0': 210, '1': 58}, 'flags': {}, 'order': 2, 'mode': 0, 'outputs': [{'name': 'VAE', 'type': 'VAE', 'links': [24], 'shape': 3, 'slot_index': 0}], 'properties': {'Node name for S&R': 'VAELoader'}, 'widgets_values': ['kl-f8-anime2.vae.pt']}, {'id': 19, 'type': 'UpscaleModelLoader', 'pos': [658, -190], 'size': {'0': 210, '1': 58}, 'flags': {}, 'order': 3, 'mode': 0, 'outputs': [{'name': 'UPSCALE_MODEL', 'type': 'UPSCALE_MODEL', 'links': [25], 'shape': 3, 'slot_index': 0}], 'properties': {'Node name for S&R': 'UpscaleModelLoader'}, 'widgets_values': ['RealESRGAN_x4plus_anime_6B.pth']}, {'id': 11, 'type': 'LoadImage', 'pos': [198, -230], 'size': {'0': 315, '1': 314.0000305175781}, 'flags': {}, 'order': 4, 'mode': 0, 'outputs': [{'name': 'IMAGE', 'type': 'IMAGE', 'links': [15, 27], 'shape': 3, 'slot_index': 0}, {'name': 'MASK', 'type': 'MASK', 'links': None, 'shape': 3}], 'properties': {'Node name for S&R': 'LoadImage'}, 'widgets_values': ['1067522a01f49e74d10359e42025fb9 (3).png', 'image']}, {'id': 20, 'type': 'SaveImage', 'pos': [1298, -552], 'size': {'0': 315, '1': 270}, 'flags': {}, 'order': 9, 'mode': 0, 'inputs': [{'name': 'images', 'type': 'IMAGE', 'link': 26}], 'properties': {}, 'widgets_values': ['ComfyUI']}, {'id': 15, 'type': 'UltimateSDUpscale', 'pos': [934, -556], 'size': {'0': 315, '1': 590}, 'flags': {}, 'order': 8, 'mode': 0, 'inputs': [{'name': 'image', 'type': 'IMAGE', 'link': 27}, {'name': 'model', 'type': 'MODEL', 'link': 21}, {'name': 'positive', 'type': 'CONDITIONING', 'link': 19}, {'name': 'negative', 'type': 'CONDITIONING', 'link': 20}, {'name': 'vae', 'type': 'VAE', 'link': 24}, {'name': 'upscale_model', 'type': 'UPSCALE_MODEL', 'link': 25}], 'outputs': [{'name': 'IMAGE', 'type': 'IMAGE', 'links': [26], 'shape': 3, 'slot_index': 0}], 'properties': {'Node name for S&R': 'UltimateSDUpscale'}, 'widgets_values': [4, 989892471729866, 'randomize', 20, 8, 'euler', 'normal', 0.4, 'Linear', 512, 512, 8, 32, 'None', 1, 64, 8, 16, 'enable']}], 'links': [[15, 11, 0, 12, 2, 'IMAGE'], [16, 13, 0, 12, 1, 'CONTROL_NET'], [18, 6, 0, 12, 0, 'CONDITIONING'], [19, 12, 0, 15, 2, 'CONDITIONING'], [20, 16, 0, 15, 3, 'CONDITIONING'], [21, 17, 0, 15, 1, 'MODEL'], [22, 17, 1, 16, 0, 'CLIP'], [23, 17, 1, 6, 0, 'CLIP'], [24, 18, 0, 15, 4, 'VAE'], [25, 19, 0, 15, 5, 'UPSCALE_MODEL'], [26, 15, 0, 20, 0, 'IMAGE'], [27, 11, 0, 15, 0, 'IMAGE']], 'groups': []
                                                     , 'config': {}, 'extra': {}, 'version': 0.4}}, 'client_id': 'ce4208d823504f739765b7b5451235bf'}


line_art = {
    '15': {
        'inputs': {
            'image': 'Screenshot 2023-11-04 201915 (1).png',
            'choose file to upload': 'image'
        },
        'class_type': 'LoadImage'
    },
    '17': {
        'inputs': {
            'pixels': ['41', 0],
            'vae': ['26', 0]
        },
        'class_type': 'VAEEncode'
    },
    '18': {
        'inputs': {
            'ckpt_name': 'etherBluMix_etherBluMix5.safetensors'
        },
        'class_type': 'CheckpointLoaderSimple'
    },
    '19': {
        'inputs': {
            'text': 'monochrome, lineart, greyscale,monochrome,line art, black and white, clean, complete drawing, completed, not too many lines, long lines, long strokes, less lines, combined lines, not so many lines, one stroke,',
            'clip': ['53', 1]
        },
        'class_type': 'CLIPTextEncode'
    },
    '23': {
        'inputs': {
            'text': 'color, EasyNegative',
            'clip': ['53', 1]
        },
        'class_type': 'CLIPTextEncode'
    },
    '26': {
        'inputs': {
            'vae_name': 'kl-f8-anime2.vae.pt'
        },
        'class_type': 'VAELoader'
    },
    '29': {
        'inputs': {
            'seed': 859806481806324,
            'steps': 20,
            'cfg': 7.0,
            'sampler_name': 'dpmpp_2m_sde_gpu',
            'scheduler': 'karras',
            'denoise': 0.4,
            'model': ['53', 0],
            'positive': ['19', 0],
            'negative': ['23', 0],
            'latent_image': ['17', 0]
        },
        'class_type': 'KSampler'
    },
    '41': {
        'inputs': {
            'upscale_method': 'nearest-exact',
            'scale_by': 1.0,
            'image': ['15', 0]
        },
        'class_type': 'ImageScaleBy'
    },
    '43': {
        'inputs': {
            'samples': ['29', 0],
            'vae': ['26', 0]
        },
        'class_type': 'VAEDecode'
    },
    '46': {
        'inputs': {
            'filename_prefix': 'ComfyUI',
            'images': ['43', 0]
        },
        'class_type': 'SaveImage'
    },
    '53': {
        'inputs': {
            'lora_name': 'animeoutlineV4_16.safetensors',
            'strength_model': 0.7000000000000001,
            'strength_clip': 0.5,
            'model': ['54', 0],
            'clip': ['54', 1]
        },
        'class_type': 'LoraLoader'
    },
    '54': {
        'inputs': {
            'lora_name': 'lineartLora_V1.0.safetensors',
            'strength_model': 0.2,
            'strength_clip': 0.5,
            'model': ['18', 0],
            'clip': ['18', 1]
        },
        'class_type': 'LoraLoader'
    }
}


line_art_extra_data = {}
line_art_execute_outputs = ['46']


SDXL = {
  "3": {
    "inputs": {
      "seed": 1000,
      "steps": 30,
      "cfg": 10,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 0.9500000000000001,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "12",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "SDXLAnimeBulldozer_v10.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "6": {
    "inputs": {
      "text": "",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "text, watermark, negativeXL_D,unaestheticXL_hk1,photorealistic,3d model,cinematic,bad anatomy,blurry,disembodied limb,worst quality,low quality,More than five fingers in one hand,More than 5 toes on one foot,hand with more than 5 fingers,hand with less than 4 fingers,ad anatomy,bad hands,mutated hands and fingers,extra legs,extra arms,interlocked fingers,duplicate,cropped,text,jpeg,artifacts,signature,watermark,username,blurry,artist name,trademark,title,muscular,sd character,multiple view,Reference sheet,long body,malformed limbs,multiple breasts,cloned face,malformed,mutated,bad anatomy,disfigured,bad proportions,duplicate,bad feet,artist name,extra limbs,ugly,fused anus,text font ui,missing limb, 1 coffee cup",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "11": {
    "inputs": {
      "image": "preprocesstest.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "12": {
    "inputs": {
      "pixels": [
        "11",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  }
}

SDXL_data = {
  "last_node_id": 13,
  "last_link_id": 22,
  "nodes": [
    {
      "id": 8,
      "type": "VAEDecode",
      "pos": [
        1209,
        188
      ],
      "size": {
        "0": 210,
        "1": 46
      },
      "flags": {},
      "order": 6,
      "mode": 0,
      "inputs": [
        {
          "name": "samples",
          "type": "LATENT",
          "link": 7
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 8
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            9
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "VAEDecode"
      }
    },
    {
      "id": 6,
      "type": "CLIPTextEncode",
      "pos": [
        -32,
        -31
      ],
      "size": {
        "0": 422.84503173828125,
        "1": 164.31304931640625
      },
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [
        {
          "name": "clip",
          "type": "CLIP",
          "link": 16
        }
      ],
      "outputs": [
        {
          "name": "CONDITIONING",
          "type": "CONDITIONING",
          "links": [
            18
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "CLIPTextEncode"
      },
      "widgets_values": [
        "1girl, cup, solo, blonde hair, long hair, window, coffee, cafe, jewelry, earrings, blush, sitting, saucer, table, indoors, bangs, long sleeves, sleeves past wrists, blurry, teacup, collarbone, blue eyes, looking away, looking outside, sweater, hair bow, standing up, cold, winter, lights, night lights. next to the sea, europe, <Lora:Vivid_Impactful_Style_locon_v4h.safetensors:0.7>, extremely detailed, beautiful, colored, really colorful, Yoneyama Mai, Hiten, Mignon, cute, 4k, city skyline in the distance"
      ]
    },
    {
      "id": 7,
      "type": "CLIPTextEncode",
      "pos": [
        -41,
        346
      ],
      "size": {
        "0": 425.27801513671875,
        "1": 180.6060791015625
      },
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {
          "name": "clip",
          "type": "CLIP",
          "link": 17
        }
      ],
      "outputs": [
        {
          "name": "CONDITIONING",
          "type": "CONDITIONING",
          "links": [
            6
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "CLIPTextEncode"
      },
      "widgets_values": [
        "text, watermark, negativeXL_D,unaestheticXL_hk1,photorealistic,3d model,cinematic,bad anatomy,blurry,disembodied limb,worst quality,low quality,More than five fingers in one hand,More than 5 toes on one foot,hand with more than 5 fingers,hand with less than 4 fingers,ad anatomy,bad hands,mutated hands and fingers,extra legs,extra arms,interlocked fingers,duplicate,cropped,text,jpeg,artifacts,signature,watermark,username,blurry,artist name,trademark,title,muscular,sd character,multiple view,Reference sheet,long body,malformed limbs,multiple breasts,cloned face,malformed,mutated,bad anatomy,disfigured,bad proportions,duplicate,bad feet,artist name,extra limbs,ugly,fused anus,text font ui,missing limb, 1 coffee cup"
      ]
    },
    {
      "id": 12,
      "type": "VAEEncode",
      "pos": [
        584,
        452
      ],
      "size": {
        "0": 210,
        "1": 46
      },
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [
        {
          "name": "pixels",
          "type": "IMAGE",
          "link": 19
        },
        {
          "name": "vae",
          "type": "VAE",
          "link": 21
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            20
          ],
          "shape": 3
        }
      ],
      "properties": {
        "Node name for S&R": "VAEEncode"
      }
    },
    {
      "id": 3,
      "type": "KSampler",
      "pos": [
        863,
        186
      ],
      "size": {
        "0": 315,
        "1": 262
      },
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [
        {
          "name": "model",
          "type": "MODEL",
          "link": 15
        },
        {
          "name": "positive",
          "type": "CONDITIONING",
          "link": 18
        },
        {
          "name": "negative",
          "type": "CONDITIONING",
          "link": 6
        },
        {
          "name": "latent_image",
          "type": "LATENT",
          "link": 20,
          "slot_index": 3
        }
      ],
      "outputs": [
        {
          "name": "LATENT",
          "type": "LATENT",
          "links": [
            7
          ],
          "slot_index": 0
        }
      ],
      "properties": {
        "Node name for S&R": "KSampler"
      },
      "widgets_values": [
        1000,
        "fixed",
        35,
        10,
        "euler",
        "karras",
        0.9500000000000001
      ]
    },
    {
      "id": 4,
      "type": "CheckpointLoaderSimple",
      "pos": [
        -561,
        215
      ],
      "size": {
        "0": 315,
        "1": 98
      },
      "flags": {},
      "order": 0,
      "mode": 0,
      "outputs": [
        {
          "name": "MODEL",
          "type": "MODEL",
          "links": [
            15
          ],
          "slot_index": 0
        },
        {
          "name": "CLIP",
          "type": "CLIP",
          "links": [
            16,
            17
          ],
          "slot_index": 1
        },
        {
          "name": "VAE",
          "type": "VAE",
          "links": [
            8,
            21
          ],
          "slot_index": 2
        }
      ],
      "properties": {
        "Node name for S&R": "CheckpointLoaderSimple"
      },
      "widgets_values": [
        "SDXLAnimeBulldozer_v10.safetensors"
      ]
    },
    {
      "id": 11,
      "type": "LoadImage",
      "pos": [
        235,
        626
      ],
      "size": [
        315,
        314.00000381469727
      ],
      "flags": {},
      "order": 1,
      "mode": 0,
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "links": [
            19
          ],
          "shape": 3,
          "slot_index": 0
        },
        {
          "name": "MASK",
          "type": "MASK",
          "links": [],
          "shape": 3,
          "slot_index": 1
        }
      ],
      "properties": {
        "Node name for S&R": "LoadImage"
      },
      "widgets_values": [
        "preprocesstest.png",
        "image"
      ]
    },
    {
      "id": 9,
      "type": "SaveImage",
      "pos": [
        1431,
        207
      ],
      "size": {
        "0": 210,
        "1": 270
      },
      "flags": {},
      "order": 7,
      "mode": 0,
      "inputs": [
        {
          "name": "images",
          "type": "IMAGE",
          "link": 9
        }
      ],
      "properties": {},
      "widgets_values": [
        "ComfyUI"
      ]
    }
  ],
  "links": [
    [
      6,
      7,
      0,
      3,
      2,
      "CONDITIONING"
    ],
    [
      7,
      3,
      0,
      8,
      0,
      "LATENT"
    ],
    [
      8,
      4,
      2,
      8,
      1,
      "VAE"
    ],
    [
      9,
      8,
      0,
      9,
      0,
      "IMAGE"
    ],
    [
      15,
      4,
      0,
      3,
      0,
      "MODEL"
    ],
    [
      16,
      4,
      1,
      6,
      0,
      "CLIP"
    ],
    [
      17,
      4,
      1,
      7,
      0,
      "CLIP"
    ],
    [
      18,
      6,
      0,
      3,
      1,
      "CONDITIONING"
    ],
    [
      19,
      11,
      0,
      12,
      0,
      "IMAGE"
    ],
    [
      20,
      12,
      0,
      3,
      3,
      "LATENT"
    ],
    [
      21,
      4,
      2,
      12,
      1,
      "VAE"
    ]
  ],
  "groups": [],
  "config": {},
  "extra": {},
  "version": 0.4
}
SDXL_outputs = ['9']


SDXLrembg ={
  "3": {
    "inputs": {
      "seed": 1000,
      "steps": 35,
      "cfg": 8,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 0.900000000000001,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "12",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "SDXLAnimeBulldozer_v10.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "6": {
    "inputs": {
      "text": "1girl, cup, solo, blonde hair, long hair, window, coffee, cafe, jewelry, earrings, blush, sitting, saucer, table, indoors, bangs, long sleeves, sleeves past wrists, blurry, teacup, collarbone, blue eyes, looking away,  sweater, hair bow, standing up, cold, winter, lights, europe, extremely detailed, beautiful, colored, really colorful, Yoneyama Mai, Hiten, Mignon, cute, 4k, ",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "text, watermark, negativeXL_D,unaestheticXL_hk1,photorealistic,3d model,cinematic,bad anatomy,blurry,disembodied limb,worst quality,low quality,More than five fingers in one hand,More than 5 toes on one foot,hand with more than 5 fingers,hand with less than 4 fingers,ad anatomy,bad hands,mutated hands and fingers,extra legs,extra arms,interlocked fingers,duplicate,cropped,text,jpeg,artifacts,signature,watermark,username,blurry,artist name,trademark,title,muscular,sd character,multiple view,Reference sheet,long body,malformed limbs,multiple breasts,cloned face,malformed,mutated,bad anatomy,disfigured,bad proportions,duplicate,bad feet,artist name,extra limbs,ugly,fused anus,text font ui,missing limb, 1 coffee cup",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "12": {
    "inputs": {
      "pixels": [
        "16",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "14": {
    "inputs": {
      "image": [
        "8",
        0
      ]
    },
    "class_type": "Image Remove Background (rembg)",
    "_meta": {
      "title": "Image Remove Background (rembg)"
    }
  },
  "15": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "14",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "16": {
    "inputs": {
      "image": "example.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  }
}

SDXLrembg_output = ['15']




LineArtNew = {
  "3": {
    "inputs": {
      "seed": 1000,
      "steps": 20,
      "cfg": 10,
      "sampler_name": "euler",
      "scheduler": "karras",
      "denoise": 0.50,
      "model": [
        "17",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "18",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "ghostmix_v20Bakedvae.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "6": {
    "inputs": {
      "text": "perfect lines, whitebackground, <lora:LineArt-60.safetensors:0.7>",
      "clip": [
        "17",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "blurry, gray scale, not sharp",
      "clip": [
        "17",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "17": {
    "inputs": {
      "lora_name": "LineArt-60.safetensors",
      "strength_model": 0.5,
      "strength_clip": 0.5,
      "model": [
        "4",
        0
      ],
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "Load LoRA"
    }
  },
  "18": {
    "inputs": {
      "pixels": [
        "19",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "19": {
    "inputs": {
      "image": "preprocesstest.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "20": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "63": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "20",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}

LineArtNew_output = ['63']

LineArtSDXL = {
  "3": {
    "inputs": {
      "seed": 272468417966614,
      "steps": 20,
      "cfg": 10,
      "sampler_name": "dpmpp_3m_sde",
      "scheduler": "karras",
      "denoise": 0.8,
      "model": [
        "14",
        0
      ],
      "positive": [
        "16",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "12",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "nablaThetaA5LinesAndColors_v10.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "6": {
    "inputs": {
      "text": "MAI SAKURAJIMA, LONG HAIR, BANGS, (BLACK HAIR:1.5), HAIR ORNAMENT, (PURPLE EYES:1.1), HAIRCLIP, RABBIT HAIR ORNAMENT,\nSKIRT, SHIRT, SCHOOL UNIFORM, WHITE SHIRT, SHORT SLEEVES, PANTYHOSE, PLEATED SKIRT, COLLARED SHIRT, BLUE SKIRT, BLACK PANTYHOSE, RED NECKTIE, JACKET, (BROWN JACKET:1.5),\nBOW, ANIMAL EARS, CLEAVAGE, BARE SHOULDERS, PANTYHOSE, BOWTIE, BLACK FOOTWEAR, RABBIT EARS, HIGH HEELS, LEOTARD, BLACK PANTYHOSE, STRAPLESS, BLACK BOW, DETACHED COLLAR, FAKE ANIMAL EARS, PLAYBOY BUNNY, BLACK LEOTARD, STRAPLESS LEOTARD, THIGHBAND PANTYHOSE, BLACK BOWTIE, 1 girl",
      "clip": [
        "14",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "text, watermark, negativeXL_D,unaestheticXL_hk1,photorealistic,3d model,cinematic,bad anatomy,blurry,disembodied limb,worst quality,low quality,More than five fingers in one hand,More than 5 toes on one foot,hand with more than 5 fingers,hand with less than 4 fingers,ad anatomy,bad hands,mutated hands and fingers,extra legs,extra arms,interlocked fingers,duplicate,cropped,text,jpeg, sketch, rough lines, colorful, colors, multiple colors, way too many colors, ines, colored",
      "clip": [
        "14",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "11": {
    "inputs": {
      "image": "preprocesstest.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "12": {
    "inputs": {
      "pixels": [
        "11",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "14": {
    "inputs": {
      "lora_name": "LineArt2.safetensors",
      "strength_model": 0.05,
      "strength_clip": 0.05,
      "model": [
        "4",
        0
      ],
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "Load LoRA"
    }
  },
  "15": {
    "inputs": {
      "control_net_name": "controlnetMyseeEdgeDrawing_02.safetensors"
    },
    "class_type": "ControlNetLoader",
    "_meta": {
      "title": "Load ControlNet Model"
    }
  },
  "16": {
    "inputs": {
      "strength": 0.35000000000000003,
      "conditioning": [
        "6",
        0
      ],
      "control_net": [
        "15",
        0
      ],
      "image": [
        "11",
        0
      ]
    },
    "class_type": "ControlNetApply",
    "_meta": {
      "title": "Apply ControlNet"
    }
  },
  "19": {
    "inputs": {
      "samples": [
        "23",
        0
      ],
      "vae": [
        "25",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "21": {
    "inputs": {
      "filename_prefix": "ComclientOutput",
      "images": [
        "19",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "22": {
    "inputs": {
      "pixels": [
        "8",
        0
      ],
      "vae": [
        "25",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "23": {
    "inputs": {
      "seed": 492262355106576,
      "steps": 20,
      "cfg": 10,
      "sampler_name": "dpmpp_3m_sde",
      "scheduler": "karras",
      "denoise": 0.4,
      "model": [
        "25",
        0
      ],
      "positive": [
        "27",
        0
      ],
      "negative": [
        "28",
        0
      ],
      "latent_image": [
        "22",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "25": {
    "inputs": {
      "ckpt_name": "SDXLAnimeBulldozer_v10.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "27": {
    "inputs": {
      "text": "MAI SAKURAJIMA, LONG HAIR, BANGS, (BLACK HAIR:1.5), HAIR ORNAMENT, (PURPLE EYES:1.1), HAIRCLIP, RABBIT HAIR ORNAMENT,\nSKIRT, SHIRT, SCHOOL UNIFORM, WHITE SHIRT, SHORT SLEEVES, PANTYHOSE, PLEATED SKIRT, COLLARED SHIRT, BLUE SKIRT, BLACK PANTYHOSE, RED NECKTIE, JACKET, (BROWN JACKET:1.5),\nBOW, ANIMAL EARS, CLEAVAGE, BARE SHOULDERS, PANTYHOSE, BOWTIE, BLACK FOOTWEAR, RABBIT EARS, HIGH HEELS, LEOTARD, BLACK PANTYHOSE, STRAPLESS, BLACK BOW, DETACHED COLLAR, FAKE ANIMAL EARS, PLAYBOY BUNNY, BLACK LEOTARD, STRAPLESS LEOTARD, THIGHBAND PANTYHOSE, BLACK BOWTIE,1 girl",
      "clip": [
        "25",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "28": {
    "inputs": {
      "text": "text, watermark, negativeXL_D,unaestheticXL_hk1,photorealistic,3d model,cinematic,bad anatomy,blurry,disembodied limb,worst quality,low quality,More than five fingers in one hand,More than 5 toes on one foot,hand with more than 5 fingers,hand with less than 4 fingers,ad anatomy,bad hands,mutated hands and fingers,extra legs,extra arms,interlocked fingers,duplicate,cropped,text,jpeg, sketch, rough lines, colorful, colors, multiple colors, way too many colors, ines, colored",
      "clip": [
        "25",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  }
}



LineArtSDXL_outputs = ['21']