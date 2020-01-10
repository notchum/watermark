"""
    Author:   Morgan Chumbley
    Date:     January 9, 2020
    Version:  1.3
    Title:    watermark.py
    Purpose:  
"""

import numpy as np
import cv2, os, argparse
from imutils import paths

INVERT = False

def resizeImage(img, scale):
    # resize image
    scale_percent = scale # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

    return resized

def makeWM(img):
    if(len(img.shape) == 2):
        colorImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif(len(img.shape) == 3):
        colorImg = img
    _, alpha = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(colorImg)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba)

    (B, G, R, A) = cv2.split(dst)
    B = cv2.bitwise_and(B, B, mask=A)
    G = cv2.bitwise_and(G, G, mask=A)
    R = cv2.bitwise_and(R, R, mask=A)
    watermark = cv2.merge([B, G, R, A])

    return watermark

def cropOutText(img):
    # Convert to GS and binarize with a threshold of 1
    if(len(img.shape) == 2):
        gray = img
    if(len(img.shape) == 3):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    dilated = cv2.dilate(thresh,kernel,iterations = 50) # dilate
    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)

        # # discard areas that are too large
        # if h>300 and w>300:
        #     continue

        # # discard areas that are too small
        if h<40 or w<40:
            continue

        # draw rectangle around contour on original image
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)

    # Crop the image
    crop = img[y:y + h, x:x + w]

    return crop

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--watermark", required=True,
	help="path to watermark image (assumed to be transparent PNG)")
ap.add_argument("-i", "--input", required=True,
	help="path to the input directory of image(s)")
ap.add_argument("-o", "--output", required=False,
	help="path to the output directory")
ap.add_argument("-f", "--filename", required=False,
	help="name of new file")
ap.add_argument("-b", "--bulk_mode", type=int, default=1,
	help="flag used to handle if bulk mode is active")
ap.add_argument("-s", "--scale", type=int, default=80,
	help="scale of input watermark image")
ap.add_argument("-p", "--position", type=str, default="lower_right",
	help="position of the watermark on output image(s)")
ap.add_argument("-a", "--alpha", type=float, default=0.80,
	help="alpha transparency of the overlay (smaller is more transparent)")
ap.add_argument("-c", "--correct", type=int, default=1,
	help="flag used to handle if bug is displayed or not")
ap.add_argument("-n", "--negate", type=bool, default=False,
	help="flag used to handle if watermark is inverted or not")
args = vars(ap.parse_args())

# Main
if __name__ == '__main__':
    # If bulk mode is selected without an output directory, throw error
    if args["bulk_mode"] and args["output"] is None:
        ap.error("--bulk_mode requires --output.")
    elif args["bulk_mode"] == 0 and args["filename"] is None:
        ap.error("!--bulk_mode requires --filename")

    # Read the watermark and adjust scale
    print("Adjusting watermark...")
    watermark = cv2.imread(args["watermark"], cv2.IMREAD_GRAYSCALE)
    watermark = resizeImage(watermark, args["scale"])
    watermark = cropOutText(watermark)
    (wH, wW) = watermark.shape[:2]
 
    # Used for debugging, but this applies transparency
    if args["correct"] > 0:
        watermark = makeWM(watermark)

    # If inverted watermark is selected then negate
    INVERT = args["negate"]
    if INVERT:
        print("Inverting watermark...")
        watermark = cv2.bitwise_not(watermark)

    # If bulk imaging is selected
    if args["bulk_mode"]:
        print("Applying watermark to images in bulk...")

        # loop over the input images
        for imagePath in paths.list_images(args["input"]):
            # load the input image, then add an extra dimension to the
            # image (i.e., the alpha transparency)
            image = cv2.imread(imagePath)
            (h, w) = image.shape[:2]
            image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])
        
            # construct an overlay that is the same size as the input
            # image, (using an extra dimension for the alpha transparency),
            # then add the watermark to the overlay in the bottom-right
            # corner
            overlay = np.zeros((h, w, 4), dtype="uint8")
            if args["position"] == "lower_right":
                overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark
            elif args["position"] == "lower_center":
                overlay[h - wH - 10:h - 10, w//2 - wW//2:w//2 - wW//2 + wW] = watermark
            elif args["position"] == "lower_left":
                overlay[h - wH - 10:h - 10, 10:wW + 10] = watermark
            elif args["position"] == "middle_right":
                overlay[h//2 - wH//2:h//2 - wH//2 + wH, w - wW - 10:w - 10] = watermark
            elif args["position"] == "middle_center":
                overlay[h//2 - wH//2:h//2 - wH//2 + wH, w//2 - wW//2:w//2 - wW//2 + wW] = watermark
            elif args["position"] == "middle_left":
                overlay[h//2 - wH//2:h//2 - wH//2 + wH, 10:wW + 10] = watermark
            elif args["position"] == "upper_right":
                overlay[10:wH + 10, w - wW - 10:w - 10] = watermark
            elif args["position"] == "upper_center":
                overlay[10:wH + 10, w//2 - wW//2:w//2 - wW//2 + wW] = watermark
            elif args["position"] == "upper_left":
                overlay[10:wH + 10, 10:wW + 10] = watermark
        
            # blend the two images together using transparent overlays
            output = image.copy()
            cv2.addWeighted(overlay, args["alpha"], output, 1.0, 0, output)
        
            # write the output image to disk
            filename = imagePath[imagePath.rfind(os.path.sep) + 1:]
            p = os.path.sep.join((args["output"], filename))
            cv2.imwrite(p, output)

    # If single image selected
    else:
        print("Applying watermark to image...")
        imagePath = args["input"]

        # load the input image, then add an extra dimension to the
        # image (i.e., the alpha transparency)
        image = cv2.imread(imagePath)
        (h, w) = image.shape[:2]
        image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])
    
        # construct an overlay that is the same size as the input
        # image, (using an extra dimension for the alpha transparency),
        # then add the watermark to the overlay in the bottom-right
        # corner
        overlay = np.zeros((h, w, 4), dtype="uint8")
        if args["position"] == "lower_right":
            overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark
        elif args["position"] == "lower_center":
            overlay[h - wH - 10:h - 10, w//2 - wW//2:w//2 - wW//2 + wW] = watermark
        elif args["position"] == "lower_left":
            overlay[h - wH - 10:h - 10, 10:wW + 10] = watermark
        elif args["position"] == "middle_right":
            overlay[h//2 - wH//2:h//2 - wH//2 + wH, w - wW - 10:w - 10] = watermark
        elif args["position"] == "middle_center":
            overlay[h//2 - wH//2:h//2 - wH//2 + wH, w//2 - wW//2:w//2 - wW//2 + wW] = watermark
        elif args["position"] == "middle_left":
            overlay[h//2 - wH//2:h//2 - wH//2 + wH, 10:wW + 10] = watermark
        elif args["position"] == "upper_right":
            overlay[10:wH + 10, w - wW - 10:w - 10] = watermark
        elif args["position"] == "upper_center":
            overlay[10:wH + 10, w//2 - wW//2:w//2 - wW//2 + wW] = watermark
        elif args["position"] == "upper_left":
            overlay[10:wH + 10, 10:wW + 10] = watermark
    
        # blend the two images together using transparent overlays
        output = image.copy()
        cv2.addWeighted(overlay, args["alpha"], output, 1.0, 0, output)

        cv2.imwrite(args["filename"], output)

    print("Finished!")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()