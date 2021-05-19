#!/usr/bin/env python
"""
Specify filepath of image with text, find number of letters in the image, save three images as jpg (image with region of interest (ROI), image cropped to ROI, and image with contours around letters)
Optionally, one can define the x and y coordinates of the start and end of the ROI in the command line. If nothing is specified the script will use the image script and predefined parameters to define the ROI.

Parameters:
    filepath: str <filepath-to-image>
    output_folder: str <name-of-output-folder>
    x_start: int <start-of-ROI-on-x-axis>
    x_end: int <end-of-ROI-on-x-axis>
    y_start: int <start-of-ROI-on-y-axis>
    y_end: int <end-of-ROI-on-y-axis>
    
Usage:
    edge_detection.py -f <filepath-to-image> -o <name-of-output-folder> -x_s <start-on-x-axis> -x_e <end-on-x-axis> -y_s <start-on-y-axis> -y_e <end-on-y-axis>

Example:
    $ python3 edge_detection.py -f ../data/Jefferson_Memorial.jpg -o out -x_s 1410 -x_e 2840 -y_s 880 -y_e 2800
    
## Task
- Use computer vision to extract specific features from images and save intermediate steps as .jpg
"""

# importing libraries
import os
import sys
sys.path.append(os.path.join(".."))
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse


# argparse 
ap = argparse.ArgumentParser()
# adding arguments for input and output filepath
ap.add_argument("-f", "--filepath", required = True, help= "Filepath to image")
ap.add_argument("-o", "--output_folder", default = "out", help = "Name of output folder")
# adding arguments to define region of interest
ap.add_argument("-x_s", "--x_start", required = False, help = "Start of region of interest on the x-axis")
ap.add_argument("-x_e", "--x_end", required = False, help = "End of region of interest on the x-axis")
ap.add_argument("-y_s", "--y_start", required = False, help = "Start of region of interest on the y-axis")
ap.add_argument("-y_e", "--y_end", required = False, help = "End of region of interest on the y-axis")
# parsing arguments
args = vars(ap.parse_args())


def main(arguments):
    '''
    Main function:
        - Get values from argparse (if none is provided for the ROI, use image shape and set parameters)
        - Initialize edge detection class and use its methods.
    '''
    # get image filepath
    image_path = args["filepath"]
    # load image
    image = cv2.imread(image_path)
  
    # get output folder name
    out_folder = args["output_folder"]
    # make output folder
    make_out_dir(foldername = out_folder)
    
    
    # defining x and y coordinates for the ROI

    # x_start
    if args["x_start"] is None: # if no value is provided
        x_start = int(image.shape[0]//2.3) # use shape of image
    else: # else 
        x_start = int(args["x_start"]) # use user defined value
    
    # x_end
    if args["x_end"] is None:
        x_end = int(image.shape[0]//1.12)
    else:
        x_end = int(args["x_end"])
    
    # y_start
    if args["y_start"] is None:
        y_start = int(image.shape[1]//4.85)
    else:
        y_start = int(args["y_start"])
    
    # y_end
    if args["y_end"] is None:
        y_end = int(image.shape[1]//1.55)
    else:
        y_end = int(args["y_end"])
    
    # Initialize class
    edge_detection = EdgeDetect(image = image,
                                out_folder = out_folder,
                                x_start = x_start,
                                x_end = x_end,
                                y_start = y_start,
                                y_end = y_end)
    
    # Make image with region of interest overlayed in green and save it in the output folder
    edge_detection.ROI()
    
    # Crop the image to the region of interest, save it in the output folder and return it
    image_cropped = edge_detection.crop_image()
    
    # Find edges in the image and draw contours around, save image with contours and return list of contours
    contours = edge_detection.detect_edges(image_cropped = image_cropped)
    
    # Print how many contours (letters) were found on the image                             
    print(f"\nThere appears to be {len(contours)} letters in the image! OBS. some might be due to noise and artifacts...")
        

           
def make_out_dir(foldername):
    '''
    Function for making the output directory with the user defined folder name if it does not already exist.
    '''
    # Define path for directory
    dirName = os.path.join("..", foldername)
    # Create output directory if it doesn't exist in the data folder
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("\nDirectory " , dirName ,  " Created ")
    else:   
        print("\nDirectory " , dirName ,  " already exists")
        
            
class EdgeDetect:
    '''
    Class to hold the image, name of output folder, start and end of x and y pixels to use for region of interest (ROI).
    It has methods to i) define the ROI and save this superimposed on the original image, ii) crop the image to the ROI and save this and 
    iii) detect edges within the cropped image and use this for making contours over objects (letters).
    
    '''
    def __init__(self, image, out_folder, x_start, y_start, x_end, y_end):
        '''
        Initializing the class by defining the object attributes.
        '''
        self.image = image
        self.out_folder = out_folder
        self.x_start = x_start
        self.y_start = y_start 
        self.x_end = x_end
        self.y_end = y_end
        
        
    def ROI(self):
        '''
        Using the defined start and end of the region of interest to draw a rectangle on the original image.
        Saving this in the output folder as jpg.
        '''
        # defining image with green rectangular box (ROI)
        ROI_image = cv2.rectangle(self.image.copy(), (self.x_start, self.y_start), (self.x_end, self.y_end), (0,255,0), (2))
        # save ROI image as jpg
        ROI_path = os.path.join("..", self.out_folder, "image_with_ROI.jpg")
        cv2.imwrite(ROI_path, ROI_image)
        # print that file has been saved
        print(f"\nThe image with the region of interest is saved as {ROI_path}")

    
    def crop_image(self):
        '''
        Cropping the original image to the extent of the ROI.
        Saving this in the output folder as jpg.
        Returns the cropped image.
        '''
        # cropping image using numpy slicing and the specified x and y coordinates
        image_cropped = self.image[self.y_start:self.y_end, self.x_start: self.x_end]
        # save cropped image as jpg
        cropped_path = os.path.join("..", self.out_folder, "image_cropped.jpg")
        cv2.imwrite(cropped_path, image_cropped)
        # print that file has been saved
        print(f"\nThe cropped image is saved as {cropped_path}")
        
        return image_cropped
    
    
    def detect_edges(self, image_cropped):
        '''
        Function for detecting edges in a cropped image.
        Converts to grey scale and blurs the image. Defines criteria for edge detection based on histogram of pixel grey scale values.
        Performs canny edge detection and uses this to find and draw contours around the edges on the original image.
        Saves the resulting image as jpg in the output folder.
        '''
        
        # Convert image to grey color scale
        grey_image = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)
        # blur using 3x3 kernel
        blurred = cv2.blur(grey_image, (3,3))
        
        # Get value of the max frequency on the greyscale using the histogram plot
        (y, x, _) = plt.hist(grey_image.flatten(), 256, [0,256])
        
        # the middle value in the range of x is where y is greatest
        x_middle = int(x[np.where(y == y.max())])
        
        # x_middle is used to define the min and max value for edge detection
        min_value = int(x_middle - 85)
        max_value = int(x_middle + 30)
        
        # canny edge detection using blurred image and range of x values that determine an edge
        canny = cv2.Canny(blurred, 
                          min_value, 
                          max_value)

        # finding and making a list of contours 
        (contours, _) = cv2.findContours(canny.copy(), # using np copy function so the contours are not overwriting the original image
                                         cv2.RETR_EXTERNAL, # keeping only the outer contours
                                         cv2.CHAIN_APPROX_SIMPLE) # stores only the corner points (alternative: CHAIN_APPROX_NONE)
        
        # drawing contours on the original image
        image_letters = cv2.drawContours(image_cropped.copy(), # draw contours on a copy of the cropped image
                                         contours, # our list of contours
                                         -1, # which contours to draw (-1 takes all at once)
                                         (0,255,0), # contour colour (this will make the contours green)
                                         2) # contour pixel width
        
        # save image with contours as jpg
        contours_path = os.path.join("..", self.out_folder, "image_letters.jpg")
        cv2.imwrite(contours_path, image_letters)
        
        # print that file has been saved
        print(f"\nThe image with contours around the letters is saved as {contours_path}")
        
        return contours
           
        
        
        
# define behavior when called from command line        
if __name__=="__main__":
    main(arguments = args)
         