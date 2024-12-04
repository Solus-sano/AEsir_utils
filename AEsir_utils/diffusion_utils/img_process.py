from PIL import Image
import numpy as np
import argparse
import os
from tqdm import tqdm




def img_crop_square(
    img_dir,
    size
):
    """
    Crops all images in the specified directory into square images and resizes them.

    This function iterates through each image file in the given directory, crops the image
    to a square by removing the longer dimension, and then resizes it to the specified size.
    The processed images overwrite the original images in the directory.

    Args:
        img_dir (str): The directory containing the images to be processed.
        size (int): The desired size to which the cropped square images will be resized.

    Raises:
        PIL.UnidentifiedImageError: If an image file cannot be identified and opened.
        OSError: If an image file cannot be saved.
    """
    for file_name in tqdm(os.listdir(img_dir)):
        try:
            img = Image.open(os.path.join(img_dir, file_name)).convert('RGB')
        except:
            continue
        # img = Image.open(os.path.join(img_dir, file_name))
        w, h = img.size
        if h>w:
            img = img.crop([0, 0, w, w])
        else:
            img = img.crop([(w-h)/2, 0, (w+h)/2, h])
        img = img.resize((size, size))
        img.save(os.path.join(img_dir, file_name))
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir', type=str, default=None)
    parser.add_argument('--size', type=int, default=512)
    args = parser.parse_args()
    img_crop_square(args.img_dir, args.size)