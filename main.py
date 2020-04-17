from __future__ import print_function
import cv2
import numpy as np
import sys
import time
import subprocess as sp
import ffmpeg

#== Parameters           
BLUR = 21
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 70
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
MASK_COLOR = (0.0,1.0,0.0) # In BGR format

cap = cv2.VideoCapture(0)
if not cap:
    sys.stdout.write("failed CaptureFromCAM")

def removeBackground(img):

    # Derived from https://stackoverflow.com/questions/49093729/remove-background-of-any-image-using-opencv
    #-- Read image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #-- Edge detection 
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    #-- Find contours in edges, sort by area 
    contour_info = []
    contours, empty2 = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    for c in contour_info:
        cv2.fillConvexPoly(mask, c[0], (255))

    #-- Smooth mask, then blur it
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background
    mask_stack = mask_stack.astype('float32') / 255.0         
    img = img.astype('float32') / 255.0    
    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR)  
    masked = (masked * 255).astype('uint8')                    
    return masked

rval, frame = cap.read()
image = cv2.imread('background.jpg');
background = cv2.resize(image, (640, 480))

lower_green = np.array([0, 150, 0])     ##[R value, G value, B value]
upper_green = np.array([50, 255, 60]) 

process = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='bgr24', s='640x480', r='30') #s='{}x{}'.format(width, height))
    .output('/dev/video1', format='v4l2', pix_fmt='yuv420p', r='30')
    .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
)

while rval:
    try:
        rval, frame = cap.read()
        key = cv2.waitKey(20)
        if frame is not None:  
            output = removeBackground(frame)
            img_copy = output.copy()
            mask = cv2.inRange(img_copy, lower_green, upper_green)
            masked_image = np.copy(img_copy)
            masked_image[mask != 0] = [0, 0, 0]
            crop_background = background.copy() #[0:720, 0:1280]
            crop_background[mask == 0] = [0, 0, 0]
            final_image = crop_background + masked_image 
            process.stdin.write(final_image) #expects a bytes type object

    except KeyboardInterrupt:
        cap.release()
        process.stdin.close()
        process.wait()
        sys.exit(0)
