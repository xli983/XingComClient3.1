from PIL import Image
from clip_interrogator import Config, Interrogator
image = Image.open("lx.jpg").convert('RGB')
ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
print(ci.interrogate_fast(image))