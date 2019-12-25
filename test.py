import cv2
import numpy as np

def cropOutText(img):
    # Convert to GS and binarize with a threshold of 1
    if(len(img.shape) == 2):
        gray = img
    if(len(img.shape) == 3):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)

        # discard areas that are too large
        if h>300 and w>300:
            continue

        # discard areas that are too small
        if h<40 or w<40:
            continue

        # draw rectangle around contour on original image
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)

    # Crop the image
    crop = img[y:y + h, x:x + w]

    return crop

def resizeImage(img, scale):
    # resize image
    scale_percent = scale # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

    return resized

def showImage(img, name):
    cv2.imshow(name, img)
    return

# Main
if __name__ == '__main__':
    watermark = cv2.imread("wmark.jpg", cv2.IMREAD_GRAYSCALE)
    watermark = resizeImage(watermark, 20)
    watermark = cropOutText(watermark)
    showImage(watermark, "cropped")

    cv2.waitKey(0)
    cv2.destroyAllWindows()