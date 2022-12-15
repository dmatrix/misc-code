import requests
from pathlib import Path
from PIL import Image, ImageFilter
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
     'https://images.pexels.com/photos/916044/pexels-photo-916044.jpeg'
 ]

SIZE = (512, 512)
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
    # Resize to a thumbnail
    img.thumbnail(SIZE)
    after_shape = img.size
    if verbose:
        print(f'{img_name} was augmented...')

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
print(f"Serial time to blur and resize {len(image_list)} images: {end - start:.2f} sec")
print(f"Original and transformed shapes: {serial_results}")

# Run distributed
print("--" * 10)
print(f"Running {len(image_list)} tasks distributed....")
start = time.perf_counter()
distributed_results = run_distributed(image_list)
end = time.perf_counter()
print(f"Distributed time to blur and resize {len(image_list)} images: {end - start:.2f} sec")
print(f"Original and transformed shapes: {distributed_results}")

assert serial_results == distributed_results
