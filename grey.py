import os, cv2

# Set the path to the directory containing the images
image_dir = 'tmp'

# Loop over all the images in the directory
for file in os.listdir(image_dir):
    # Load the image in color
    img = cv2.imread(os.path.join(image_dir, file))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(image_dir, 'gray_' + file), gray)