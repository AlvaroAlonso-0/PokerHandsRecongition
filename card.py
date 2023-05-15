import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image # type: ignore

class_list = ['B','C10', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CJ', 'CK', 'CQ', 'D10', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DJ', 'DK', 'DQ', 'H10', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'HA', 'HJ', 'HK', 'HQ', 'S10', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'SA', 'SJ', 'SK', 'SQ']
model = keras.models.load_model('model_fulldeck_v2.h5') # type: ignore

# Custom decode for predictions
def decode_predictions_custom(preds, top=3):        
    results = []
        
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [(class_list[i], pred[i]*100.0) for i in top_indices]
        results.append(result)
    return results

# Recognise cards from the image 
def recognise_cards(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours to only keep those that correspond to cards
    cards = []
    prev_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50000:  # adjust this threshold to filter out small contours
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            # card contours have four corners and if is smaller than the previous card is a figure
            if len(approx) == 4 and area-prev_area > -100000:
                cards.append(contour)
                prev_area = area
                
    predicted_cards = []                    
    
    # Rotate and display each card
    for _, card in enumerate(cards):
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

        # Get the top left corner of the card
        height, width, _ = card_img.shape
        x = int(0.12 * height)
        y = int(0.40 * width)

        # Create a new image with the left corner of the card        
        rect = card_img[0:y, 0:x]
        rect_img = np.zeros((y,x, 3), np.uint8)
        rect_img[0:y, 0:x] = rect
        
        # Call model
        var_resized = cv2.resize(rect_img, (150, 224))

        var_resized = image.img_to_array(var_resized)
        var_resized = np.expand_dims(var_resized, axis=0)
        var_resized = tf.keras.applications.imagenet_utils.preprocess_input(var_resized)
        prediction = model.predict(var_resized)

        print(decode_predictions_custom(prediction))
        
        # Decode prediction and add to list
        prediction = decode_predictions_custom(prediction)[0][0][0]
        
        if prediction != 'B':
            predicted_cards.append(prediction)
        
    cv2.destroyAllWindows()
    
    return predicted_cards