import cv2
import numpy as np

# Load image
img = cv2.imread('images/IMG_1452.jpeg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours to only keep those that correspond to cards
cards = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 10000:  # adjust this threshold to filter out small contours
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:  # card contours have four corners
            cards.append(contour)
                     
# Rotate and display each card
for i, card in enumerate(cards):
    # Get the rotated bounding box of the card contour
    rect = cv2.minAreaRect(card)
    box = cv2.boxPoints(rect)
    box = box.astype(np.int32)
    
    # Rotate the original image
    rows, cols = img.shape[:2]
    rotation = rect[2]
    if rect[2] > 45:
        rotation = 90 + rect[2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), rotation, 1)
    rotated = cv2.warpAffine(img, M, (cols, rows))

    # Transform the box to account for the rotation of the image
    points = np.array([box])
    transformed_points = cv2.transform(points, M)
    transformed_box = transformed_points[0].astype(np.int32)

    # Crop the rotated image to only show the card
    x, y, w, h = cv2.boundingRect(transformed_box)
    card_img = rotated[y:y+h, x:x+w]

    # Display the card image in a window
    cv2.imshow('Card ' + str(i+1), card_img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
