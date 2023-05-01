import cv2
import numpy as np

def recognise(card):
    final_value = ''
    final_suit = ''

    return f'{final_value} - {final_suit}'

# Load image
img = cv2.imread('images/IMG_1482.jpeg')
back = cv2.imread('images/templates/back2.png')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Detector and descriptor for matching cards
detector = cv2.ORB_create()
descriptor = cv2.ORB_create()

# Matcher
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Back key points and descriptors
back_kp, back_desc = detector.detectAndCompute(gray_back, None)

# Filter contours to only keep those that correspond to cards
cards = []
prev_area = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100000:  # adjust this threshold to filter out small contours
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        # card contours have four corners and if is smaller than the previous card is a figure
        if len(approx) == 4 and area-prev_area > -100000:
            cards.append(contour)
            prev_area = area
                     
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

    # Convert to grayscale
    grey_card = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
    
    # Calculate the key points and descriptors for the card
    card_kp, card_desc = detector.detectAndCompute(grey_card, None)
    
    # Match the card to the back
    matches = matcher.match(card_desc, back_desc)
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Calculate the similarity between the card and the back
    similarity = sum(1 for m in matches if m.distance < 0.35 * len(back_kp)) / len(back_kp)
    
    print('Similarity: ' + str(similarity))
        
    if(similarity > 0.35):
        print('Back')
    else:
        # Display the card image in a window
        #cv2.imshow('Card ' + str(i+1), card_img)
        #cv2.waitKey(0)

        height, width, channels = card_img.shape
        x = int(0.12 * height)
        y = int(0.40 * width)

        # Create a new image with the left corner of the card        
        rect = card_img[0:y, 0:x]
        rect_img = np.zeros((y,x, 3), np.uint8)
        rect_img[0:y, 0:x] = rect
        
        cv2.imwrite('Card ' + str(i+1)+ '.png', rect_img)
        #cv2.waitKey(0)
        
cv2.destroyAllWindows()
