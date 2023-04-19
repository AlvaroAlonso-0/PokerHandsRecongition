import cv2
import imutils
import numpy as np

# Load the image
image = cv2.imread('images/IMG_1228.jpeg')

# Apply pre-processing techniques
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)[1]

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
clean_contours = []
for c in contours:
    if cv2.contourArea(c) > 500000:
        clean_contours.append(c)
        
# ! ---------------------
cv2.drawContours(image, clean_contours, -1, (0, 255, 0), 3)
cv2.imshow('Card', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Load templates
suits = ['clubs', 'diamonds', 'hearts', 'spades']
values = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
suit_templates = {suit: cv2.imread(f'images/templates/{suit}.png',0) for suit in suits}
value_templates = {value: cv2.imread(f'images/templates/{value}.png',0) for value in values}

for contour in clean_contours:
    # Crop the image to the detected card region
    x, y, w, h = cv2.boundingRect(contour)
    card = image[y:y+h, x:x+w]

    # Apply pre-proessing techniques to extract suit and number
    gray_card = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)
    blur_card = cv2.GaussianBlur(gray_card, (5, 5), 0)
    thresh_card = cv2.threshold(blur_card, 120, 255, cv2.THRESH_BINARY)[1]

    # Use machine learning techniques to extract suit and value
    # Match the suit and value templates to the card image
    # Find contours in the thresholded image
    contours_roi, hierarchy_roi = cv2.findContours(thresh_card, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours_roi, key=cv2.contourArea, reverse=True)
    
    final_suit = ''
    final_value = ''
    probability_suit = 0
    probability_value = 0

    # Loop over the contours and match each to a suit or value template
    for contour in contours:
        if(cv2.contourArea(contour) < 800):
            continue
        
        print(cv2.contourArea(contour))
        cv2.drawContours(card, contour, -1, (0, 255, 0), 3)
        cv2.imshow('Card', card)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Calculate the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        # Resize the contour to match the template size
        resized_contour = cv2.resize(thresh_card[y:y+h, x:x+w], (50, 50))
        
        # Match the contour to each suit template    
        suit_scores = {}
        for suit, template in suit_templates.items():
            if resized_contour.shape[0] < template.shape[0] or resized_contour.shape[1] < template.shape[1]:
                resized_suit_contour = cv2.resize(resized_contour, (template.shape[1], template.shape[0]))
                result = cv2.matchTemplate(resized_suit_contour, template, cv2.TM_CCOEFF_NORMED)
            else:
                result = cv2.matchTemplate(resized_contour, template, cv2.TM_CCOEFF_NORMED)
            _, score, _, _ = cv2.minMaxLoc(result)
            suit_scores[suit] = score
            
        # Matched the contour to a value template
        value_scores = {}
        for value, template in value_templates.items():
            if resized_contour.shape[0] < template.shape[0] or resized_contour.shape[1] < template.shape[1]:
                resized_value_contour = cv2.resize(resized_contour, (template.shape[1], template.shape[0]))
                result = cv2.matchTemplate(resized_value_contour, template, cv2.TM_CCOEFF_NORMED)
            else:
                result = cv2.matchTemplate(resized_contour, template, cv2.TM_CCOEFF_NORMED)
            _, score, _, _ = cv2.minMaxLoc(result)
            value_scores[value] = score
            
        # Determine the suit and value of the card
        if max(suit_scores.values()) > probability_suit:
            final_suit = max(suit_scores, key=suit_scores.get) # type: ignore
            probability_suit = max(suit_scores.values())
            
        print(max(value_scores.values()), max(value_scores, key=value_scores.get)) # type: ignore
        print(max(suit_scores.values()), max(suit_scores, key=suit_scores.get)) # type: ignore
        
        if max(value_scores.values()) > probability_value:
            final_value = max(value_scores, key=value_scores.get) # type: ignore
            probability_value = max(value_scores.values())
            
    # Label the card with the suit and value
    x_text = x + 5*w
    y_text = y + 4*h
    cv2.putText(image, f'{final_value} of {final_suit}', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
        
# Display the output
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
        