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

    ct = ctimage.Segmenter(f"data/lauge-soerensen/images/subject{patientNum}_{slice}.tiff")
    ct.set_threshold(0, cv.THRESH_BINARY)
    ct.set_bgmask()
    ct.set_lung_mask_and_img()

    df = pd.DataFrame(ct.img)

    # Display the original image
    ax1 = plt.subplot(2,3,1)
    original_image = ax1.imshow(ct.img, interpolation=None, cmap='gray')
    ax1.set_title('Original Image')
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Display the thresholded image
    ax2 = plt.subplot(2,3,2)
    thresholded_image = ax2.imshow(ct.thresh_img, interpolation=None, cmap='gray')
    ax2.set_title('Binarized Image')
    ax2.set_xticks([])
    ax2.set_yticks([])

    # Mask image
    ax3 = plt.subplot(2,3,3)
    masked_image = ax3.imshow(ct.lung_img, interpolation=None, cmap='gray')
    ax3.set_title('Masked Image')
    ax3.set_xticks([])
    ax3.set_yticks([])

    # Create the frequency graph > first flatten the dataframe > filter by -1000 to 0 (Hounsfield Units) > frequency
    ax4 = plt.subplot(2,1,2)
    flat_series = df.stack()
    flat_series = flat_series[flat_series.between(-1000, 1000, inclusive='both')]
    hist, bins = np.histogram(flat_series, bins=len(flat_series.unique()))
    ax4.hist(bins[:-1], bins, weights=hist, color='gray')
    ax4.set_title("CT Scan Values")
    ax4.set_xlabel("Value")
    ax4.set_ylabel("Frequency")

    # Create a slider for the threshold value
    ax_slider = plt.axes([0.25, 0.05, 0.65, 0.03])

    slider = Slider(
        ax=ax_slider,
        label='Threshold',
        valmin=-1000,
        valmax=0,
        valinit=0,
        valstep=1
    )
    
    def update_image(val):
        threshold = int(val)
        ct.set_threshold(threshold, cv.THRESH_BINARY)
        thresholded_image.set_data(ct.thresh_img)
        
        # Making the mask
        ct.set_lung_mask_and_img()
        masked_image.set_data(ct.lung_img)
        
        plt.draw()

    slider.on_changed(update_image)

    plt.show()
