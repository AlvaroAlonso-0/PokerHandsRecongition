import cv2
import numpy as np

# Load the image
img = cv2.imread('images/IMG_1222.jpeg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to obtain binary image
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Select the contour with the largest area
contour = max(contours, key=cv2.contourArea)

# Find the bounding rectangle of the card contour
x, y, w, h = cv2.boundingRect(contour)

# Extract the region of interest (ROI) inside the card
card_roi = img[y:y+h, x:x+w]

# Convert the ROI to grayscale
gray_roi = cv2.cvtColor(card_roi, cv2.COLOR_BGR2GRAY)

# Apply thresholding to obtain binary image of the ROI
_, thresh_roi = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary ROI image
contours_roi, hierarchy_roi = cv2.findContours(thresh_roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw the contours on the original image
for contour_roi in contours_roi:
    # Offset the contour to match the position of the ROI inside the card
    contour_roi = contour_roi + (x, y)
    cv2.drawContours(img, [contour_roi], -1, (226, 220, 99), 5)

# Display the result
cv2.imshow('Card Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
