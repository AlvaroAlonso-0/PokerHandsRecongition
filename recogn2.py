import cv2

# Load the image
img = cv2.imread('images/IMG_1228.jpeg')

# Define the template images for each card
templates = {
    'AS': cv2.imread('images/templates/AS_template.jpg', 0),
    'AC': cv2.imread('images/templates/AC_template.jpg', 0),
    'AD': cv2.imread('images/templates/AD_template.jpg', 0),
    'AH': cv2.imread('images/templates/AH_template.jpg', 0)
}

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to obtain binary image
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i=0

for contour in contours:
    # Find the area of the contour
    area = cv2.contourArea(contour)
    
    # Skip the contour if it is too small
    if area < 500000:
        continue
    
    i+=1
    
    # Draw the contour on the original image
    cv2.drawContours(img, [contour], -1, (0, 255, 0), 25)

    # Find the bounding rectangle of the card contour
    x, y, w, h = cv2.boundingRect(contour)

    # Extract the region of interest (ROI) inside the card
    card_roi = img[y:y+h, x:x+w]

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(card_roi, cv2.COLOR_BGR2GRAY)

    # Loop over the templates to find the best match
    best_match = None
    best_match_score = 0
    for card, template in templates.items():
        # Apply template matching to find the match score
        res = cv2.matchTemplate(gray_roi, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, _, _ = cv2.minMaxLoc(res)
        
        # Update the best match if necessary
        if max_val > best_match_score:
            best_match = card
            best_match_score = max_val
            
    # Get the center coordinates of the card
    center_x = x + w // 2
    center_y = y + h // 2
            
    # Get the size of the text to be printed
    text_size, _ = cv2.getTextSize(best_match, cv2.FONT_HERSHEY_SIMPLEX, 12, 25)

    # Calculate the position of the text to be printed
    text_x = center_x - text_size[0] // 2
    text_y = center_y + text_size[1] // 2

    # Draw the card label on the image
    cv2.putText(img, f'{best_match} {str(i)}', (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 12, (255, 0, 0), 25)

# Display the result
cv2.imshow('Card Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
