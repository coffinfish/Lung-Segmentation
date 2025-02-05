import pydicom
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import ctimage
from matplotlib.widgets import Slider


# TO DO: NORMALIZE THE .TIFF AND DICOM FILES

# Load the DICOM file
dicom_file = pydicom.dcmread('data/cornell/PCsub1-20090909/W0001/1.2.826.0.1.3680043.2.656.1.136/S02A01/1.2.826.0.1.3680043.2.656.1.138.154.dcm',)

# Extract the pixel data from the DICOM file
img = dicom_file.pixel_array

c = -650
w = 1500
windowed_img = (img - c)/w

print(img.max(), img.min())
print(windowed_img.max(), windowed_img.min())

ax1 = plt.subplot(1,3,1)
original_image = ax1.imshow(img, interpolation=None, cmap='gray')
ax1.set_title('Original Image')
ax1.set_xticks([])
ax1.set_yticks([])

#Threshold Image
ret, thresh1 = cv.threshold(img, 0, 255, cv.THRESH_BINARY)
ax2 = plt.subplot(1,3,2)
thresholded_image = ax2.imshow(windowed_img, interpolation=None, cmap='gray')
ax2.set_title('Binarized Image')
ax2.set_xticks([])
ax2.set_yticks([])

# This basically gets most of the "lung" part by removing the background 

ret, bg_mask = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV)
lungx = ctimage.removebg(bg_mask,(0,0))
# lungx = utils.removebg(lungx,(511,511))
# lungx = utils.removebg(lungx,(0,511))
# lungx = utils.removebg(lungx,(511,0))


mask = np.zeros((img.shape[0], img.shape[1],3), dtype=np.uint16)
mask[thresh1 == 0] = [255,0,0]
mask[lungx == 0] = [0,0,0]

ax3 = plt.subplot(1,3,3)
masked_image = ax3.imshow(mask, interpolation=None)
ax3.set_title('Masked Image')
ax3.set_xticks([])
ax3.set_yticks([])



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
    ret, thresh1 = cv.threshold(img, threshold, 255, cv.THRESH_BINARY)
    thresholded_image.set_data(thresh1)
    
    # Making the mask
    mask = np.zeros((img.shape[0], img.shape[1],3), dtype=np.uint16)
    mask[thresh1 == 0] = [255,0,0]
    mask[lungx == 0] = [0,0,0]
    masked_image.set_data(mask)
    plt.draw()

# Connect the slider to the update_image function
slider.on_changed(update_image)

plt.show()


plt.show()
