import os
import pandas as pd
import random

import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
from pathlib import Path

S_TIMES = [(10, 5.71), (20, 12.86), (30, 19.94), (40, 28.64), (50, 37.89), (60, 43.91), (70, 52.8), (80, 62.12), (90, 70.86), (100, 79.23)]
D_TIMES = [(10, 2.76), (20, 4.07), (30, 5.5), (40, 9.44), (50, 10.32), (60, 11.25), (70, 13.36), (80, 16.35), (90, 20.61), (100, 21.2)]
BATCHES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

def extract_times(lst):
    s_times = [t[1] for t in lst]
    return s_times

def display_random_images(image_list, n=3):
    random_samples_idx = random.sample(range(len(image_list)), k=n)
    plt.figure(figsize=(16, 8))
    for i, targ_sample in enumerate(random_samples_idx):
        plt.subplot(1, n, i+1)
        img = Image.open(image_list[targ_sample])
        img_as_array = np.asarray(img)
        plt.imshow(img_as_array)
        title = f"\nshape: {img.size}"
        plt.axis("off")
        plt.title(title)
    plt.show()


if __name__ == "__main__":
    DATA_DIR = Path(os.getcwd() + "/task_images")

    s_times = extract_times(S_TIMES)
    d_times = extract_times(D_TIMES)
    data = {'batches': BATCHES,
            'serial' : s_times,
            'distributed': d_times}
    df = pd.DataFrame(data)
    df.plot(x="batches", y=["serial", "distributed"], kind="bar")
    plt.ylabel('Times in sec', fontsize=12)
    plt.xlabel('Number of Batches of Images', fontsize=12)
    plt.grid(False)
    plt.show()

    # # plot random images
    image_list = list(DATA_DIR.glob("*.jpg"))
    display_random_images(image_list, n=5) 
        


