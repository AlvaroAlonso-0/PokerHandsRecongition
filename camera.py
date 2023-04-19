import cv2

# Open a connection to the iPhone camera using the VideoCapture function
# with the device index set to 1 to use the iPhone camera
cap = cv2.VideoCapture(1)

# Set the video resolution to 1280x720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Loop over the video frames
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
        
    # Display the frame in a window named "iPhone Camera"
    cv2.imshow('iPhone Camera', frame)
    
    # Check if the user has pressed the "q" key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
