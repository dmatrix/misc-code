import requests
from pathlib import Path
from PIL import Image, ImageFilter
import torch
import numpy as np
from torchvision import transforms as T 
import time
import os

import ray
#
# borrowed and modified from https://analyticsindiamag.com/how-to-run-python-code-concurrently-using-multithreading/
#

URLS = [
     'https://images.pexels.com/photos/305821/pexels-photo-305821.jpeg',
     'https://images.pexels.com/photos/509922/pexels-photo-509922.jpeg',
     'https://images.pexels.com/photos/325812/pexels-photo-325812.jpeg',
     'https://images.pexels.com/photos/1252814/pexels-photo-1252814.jpeg',
     'https://images.pexels.com/photos/1420709/pexels-photo-1420709.jpeg',
     'https://images.pexels.com/photos/963486/pexels-photo-963486.jpeg',
     'https://images.pexels.com/photos/1557183/pexels-photo-1557183.jpeg',
     'https://images.pexels.com/photos/3023211/pexels-photo-3023211.jpeg',
     'https://images.pexels.com/photos/1031641/pexels-photo-1031641.jpeg',
     'https://images.pexels.com/photos/439227/pexels-photo-439227.jpeg',
     'https://images.pexels.com/photos/696644/pexels-photo-696644.jpeg',
     'https://images.pexels.com/photos/911254/pexels-photo-911254.jpeg',
     'https://images.pexels.com/photos/1001990/pexels-photo-1001990.jpeg',
     'https://images.pexels.com/photos/3518623/pexels-photo-3518623.jpeg',
     'https://images.pexels.com/photos/916044/pexels-photo-916044.jpeg',
     'https://images.pexels.com/photos/2253879/pexels-photo-2253879.jpeg',
     'https://images.pexels.com/photos/3316918/pexels-photo-3316918.jpeg',
     'https://images.pexels.com/photos/942317/pexels-photo-942317.jpeg',
     'https://images.pexels.com/photos/1090638/pexels-photo-1090638.jpeg',
     'https://images.pexels.com/photos/1279813/pexels-photo-1279813.jpeg',
     'https://images.pexels.com/photos/434645/pexels-photo-434645.jpeg',
     'https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg',
     'https://images.pexels.com/photos/1080696/pexels-photo-1080696.jpeg',
     'https://images.pexels.com/photos/271816/pexels-photo-271816.jpeg',
     'https://images.pexels.com/photos/421927/pexels-photo-421927.jpeg',
     'https://images.pexels.com/photos/302428/pexels-photo-302428.jpeg',
     'https://images.pexels.com/photos/443383/pexels-photo-443383.jpeg',
     'https://images.pexels.com/photos/3685175/pexels-photo-3685175.jpeg',
     'https://images.pexels.com/photos/2885578/pexels-photo-2885578.jpeg',
     'https://images.pexels.com/photos/3530116/pexels-photo-3530116.jpeg?'
]

THUMB_SIZE = (64, 64)
DATA_DIR = Path(os.getcwd() + "/task_images")

def download_images(url, data_dir, verbose=True):
    img_data = requests.get(url).content
    img_name = url.split("/")[4]
    img_name = f"{data_dir}/{img_name}.jpg"
    with open(img_name, 'wb+') as f:
        f.write(img_data)
        if verbose:
            print(f"downloading image to {img_name}")

def transform_image(img_name, verbose=True):
    img = Image.open(img_name)
    before_shape = img.size

    # Make the image blur with specified intensigy
    img = img.filter(ImageFilter.GaussianBlur(radius=20))
    augmentor = T.TrivialAugmentWide(num_magnitude_bins=31)
    img = augmentor(img)

    # Convert to tensor
    tensor = torch.tensor(np.asarray(img))

    # Resize to a thumbnail
    img.thumbnail(THUMB_SIZE)
    after_shape = img.size
    if verbose:
        print(f"{os.path.basename(img_name)} augmented: shape:{img.size}|original image tensor shape:{tensor.size()}")

    return before_shape, after_shape

@ray.remote
def augment_image_distributed(image):
    return transform_image(image)


def run_serially(image_list):
    transform_results = [transform_image(image) for image in image_list]
    return transform_results


def run_distributed(image_list):
    return ray.get([augment_image_distributed.remote(img) for img in image_list])

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
        for url in URLS:
            download_images(url, DATA_DIR)

image_list = list(DATA_DIR.glob("*.jpg"))

print(f"Running {len(image_list)} tasks serially....")
start = time.perf_counter()
serial_results = run_serially(image_list)
end = time.perf_counter()
print(f"\nSerial time to blur and resize {len(image_list)} images: {end - start:.2f} sec")
# print(f"Original and transformed shapes: {serial_results}")

# Run distributed
print("--" * 10)
print(f"Running {len(image_list)} tasks distributed....")
start = time.perf_counter()
distributed_results = run_distributed(image_list)
end = time.perf_counter()
print(f"\nDistributed time to blur and resize {len(image_list)} images: {end - start:.2f} sec")
# print(f"Original and transformed shapes: {distributed_results}")

assert serial_results == distributed_results
