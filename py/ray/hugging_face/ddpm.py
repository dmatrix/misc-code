from diffusers import StableDiffusionPipeline
from PIL import Image

# pipe = StableDiffusionPipeline.from_pretrained("/Users/jules/ddpm_model/")
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cpu")

prompt = "a photo of an astronaut doing headstand on mars"
image = pipe(prompt).images[0]
    
image.save("astronaut_and_butterfiles.png")
im = Image.open("astronaut_and_butterfiles.png")
image.show()