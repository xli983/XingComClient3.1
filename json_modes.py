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
            'text': 'cat ear girl, big cat ears',
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