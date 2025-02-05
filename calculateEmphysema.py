import cv2 as cv
import numpy as np
import pandas as pd
import ctimage
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


if __name__ == "__main__":
    # Select patient number
    patientNum = 1

    # Select slice (middle, top, bottom)
    slice = "middle"

    # Set Threshold
    x = -910
    ct = ctimage.Segmenter(f"data/lauge-soerensen/images/subject{patientNum}_{slice}.tiff")
    ct.set_threshold(-910, cv.THRESH_BINARY)
    ct.set_bgmask()
    ct.set_lung_mask_and_img()
    ct.calculate_emphysema()
    
    titles = ["ORIGINAL", "BINARY", "MASKED"]
    images = [ct.img, ct.thresh_img, ct.lung_img]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    for i, ax in enumerate(axes):
        ax.imshow(images[i], 'gray', vmin=0, vmax=255)
        ax.set_title(titles[i])
        ax.set_xticks([])
        ax.set_yticks([])

    plt.text(0.5, 0.05, "Percentage of Emphysema: {:.2f}%".format(ct.perc), transform=fig.transFigure, fontsize=12, 
         fontweight='bold', color='black', ha='center')

    plt.show()
