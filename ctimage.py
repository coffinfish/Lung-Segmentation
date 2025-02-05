import numpy as np
import cv2 as cv
import pandas as pd
import util


class Segmenter():
    def __init__(self, path):
        self.img = cv.imread(path, cv.IMREAD_UNCHANGED)
        assert self.img is not None, "Invalid path. check with os.path.exists()"
        self.thresh_img = None
        self.lung_img = None
        self.lung_mask = None
        self.bg_mask = None
        self.perc = None
    
    def set_threshold(self, threshold:int, type:int):
        _, self.thresh_img = cv.threshold(self.img, threshold, 255, type)
    
    def set_bgmask(self):
        ret, temp = cv.threshold(self.img, 0, 255, cv.THRESH_BINARY_INV)
        self.bg_mask = util.removebg(temp,(0,0))
    
    def set_lung_mask_and_img(self):
        # Setting the highlighted areas to red
        assert self.thresh_img is not None, "Need to set threshold first"
        assert self.bg_mask is not None, "Need to set background first"
        
        # Binary mask
        self.lung_mask = np.zeros((self.img.shape[0], self.img.shape[1]), dtype=np.uint16)
        
        self.lung_mask[self.thresh_img == 0] = 255
        # Removing the background
        self.lung_mask[self.bg_mask == 0] = 0
        
        # Making the red overlay
        self.lung_img = np.zeros((self.img.shape[0], self.img.shape[1],3), dtype=np.uint16)
        
        # Setting white pixels to red
        self.lung_img[self.lung_mask == 255] = [255, 0, 0]
    
    def calculate_emphysema(self):
        # Counting number of non zero (non black) pixels, getting a percentage of damaged lung tissue to total lung tissue
        part_lung_df = pd.DataFrame(self.lung_mask)
        total_lung_df = pd.DataFrame(self.bg_mask)
        dmg_lung = (part_lung_df != 0).sum().sum()
        total_lung = (total_lung_df != 0).sum().sum()

        # Divide the DataFrames by their respective frequencies
        self.perc = dmg_lung/total_lung * 100

        return self.perc

