from math import sqrt, radians, atan, sin, cos, pi
import numpy as np
import cv2

import argparse
import os

import numpy as np
from PIL import Image
import cv2

from .utils1 import Transforms1, Utils1


class Core1:

    def __init__(self, image):
        """
        :param image: Image holder object to perform operations on.
        """
        self.image = image
        self._shape = image.shape

    def simulate(self, simulated_recolored=False):
        """
        :param input_path: Input path of the image.
        :param simulate_type: Type of simulation needed. Can be 'protanopia', 'deutranopia', 'tritanopia', 'hybrid'.
        :param simulate_degree_primary: Primary degree of simulation: used for 'protanopia', 'deutranopia', 'tritanopia'
        :param simulate_degree_sec: Secondnary degree of simulation: used for 'hybrid'.
        :param return_type: How to return the Simulated Image. Use 'pil' for PIL.Image, 'np' for Numpy array,
                            'save' for Saving to path.
        :param save_path: Where to save the simulated file. Valid only if return_type is set as 'save'.
        :return:
        """

        # Load the image file in LMS colorspace
        if simulated_recolored == True:
            img_lms = Utils1.load_lms(self.recolored)
        else:
            img_lms = Utils1.load_lms(self.image)
            
        transform = Transforms1.lms_protanopia_sim()
        
        # Transforming the LMS Image
        img_sim = np.dot(img_lms, transform)
        
        # Converting back to RGB colorspace
        img_sim = np.uint8(np.dot(img_sim, Transforms1.lms_to_rgb()) * 255)
        
        # return img_sim
        if simulated_recolored == True:
            self.simulated_recolored_image = img_sim
        else:
            self.simulated_image = img_sim


    def correct(self):
        """
        Use this method to correct images for People with Colorblindness. The images can be corrected for anyone
        having either protanopia, deutranopia, or both. Pass protanopia_degree and deutranopia_degree as diagnosed
        by a doctor using Ishihara test.
        :param input_path: Input path of the image.
        :param protanopia_degree: Protanopia degree as diagnosed by doctor using Ishihara test.
        :param deutranopia_degree: Deutranopia degree as diagnosed by doctor using Ishihara test.
        :param return_type: How to return the Simulated Image. Use 'pil' for PIL.Image, 'np' for Numpy array,
                            'save' for Saving to path.
        :param save_path: Where to save the simulated file. Valid only if return_type is set as 'save'.
        """

        img_rgb = Utils1.load_rgb(self.image)

        transform = Transforms1.correction_matrix()

        img_corrected = np.uint8(np.dot(img_rgb, transform) * 255)
        
        # return img_corrected
        self.recolored = img_corrected


