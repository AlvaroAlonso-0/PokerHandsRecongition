import cv2
from card import *
from montecarlo import *

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
    
    key = cv2.waitKey(1) & 0xFF
    # Take a screenshot of the frame and call the recognise_cards function
    if key == ord('p'):
        print('Recognising cards...')
        cv2.imwrite('images/table.png', frame.copy())
        cards = recognise_cards(cv2.imread('images/IMG_1452.jpeg'))
        
        # Check if repeated cards
        if(len(cards) != len(set(cards))):
            print("ERROR: Repeated cards")
            continue
        
        # Get the pocket cards and community cards        
        pocket_cards_h1 = cards[-2:]
        pocket_cards_h2 = cards[-4:-2]
        community_cards = cards[:-4]
        
        print('Simulating game...')
        simulation = simulate_game([pocket_cards_h1,pocket_cards_h2], community_cards)
        
        
        # Stage of the game
        if(len(community_cards) == 0):
            print('Pre-flop')
        elif(len(community_cards) == 3):
            print('Flop')
        elif(len(community_cards) == 4):
            print('Turn')
        elif(len(community_cards) == 5):
            print('River')
            
        print(f'Hand 1 {str(pocket_cards_h1)}: {simulation[0]*100}%')
        print(f'Hand 2 {str(pocket_cards_h2)}: {simulation[1]*100}%')
        print(f'Draw: {simulation[2]*100}%')
        print('Community: ' + str(community_cards))
        
    
    # Check if the user has pressed the "q" key to quit
    if key & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
