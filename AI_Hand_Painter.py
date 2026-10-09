import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# 1. Setup Camera and Resolution
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize detector for 1 hand with high confidence
detector = HandDetector(detectionCon=0.85, maxHands=1)

# Persistent drawing layers
xp, yp = 0, 0
canvas = None

print("PRO AI Black Ink Canvas Active! ☝️ = Draw | ✌️ = Hover | Press 'c' to Clear Canvas")

while True:
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1) # Mirror effect for natural writing
    
    # Initialize blank drawing canvas layer on the very first frame
    if canvas is None:
        canvas = np.zeros_like(frame)
        
    # Track the hand (draw=True shows the visual skeleton frame smoothly)
    hands, frame = detector.findHands(frame, draw=True)
    
    # Check if a hand is actively detected on screen
    if hands:
        # Extract the dictionary for the first hand from the list index safely
        hand1 = hands[0]
        lmList = hand1["lmList"]      # 21 Landmark points
        fingers = detector.fingersUp(hand1)  # [Thumb, Index, Middle, Ring, Pinky]
        
        # Grab the precise X and Y pixels of your Index finger tip (Landmark 8)
        cx, cy = lmList[8][0], lmList[8][1]
        
        # --- GESTURE 1: DRAW MODE (Index finger UP, Middle finger DOWN) ---
        if fingers[1] == 1 and fingers[2] == 0:
            # Draw a brush target point onto the live webcam frame
            cv2.circle(frame, (cx, cy), 12, (0, 0, 255), cv2.FILLED)
            
            # Anchor drawing baseline if starting a new line sequence
            if xp == 0 and yp == 0:
                xp, yp = cx, cy
                
            # Draw a thick, high-definition white mask line onto our canvas layer
            # We use white (255, 255, 255) here so we can mask it out to black later
            cv2.line(canvas, (xp, yp), (cx, cy), (255, 255, 255), 14, cv2.LINE_AA)
            
            # Slide tracking points forward continuously
            xp, yp = cx, cy
            
        # --- GESTURE 2: HOVER MODE (Both Index and Middle fingers are raised UP) ---
        elif fingers[1] == 1 and fingers[2] == 1:
            xp, yp = 0, 0  # Sever the line path cleanly so it doesn't drag ink across screen
            cv2.circle(frame, (cx, cy), 12, (255, 0, 0), cv2.FILLED)  # Blue hover cursor
            
    else:
        # Reset tracking paths instantly if hand leaves the camera frame entirely
        xp, yp = 0, 0

    # --- GLITCH-FREE BLACK INK ENGINE ---
    # Convert our canvas lines into a clear gray map
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    # Turn everything you drew into a sharp inverse mask
    _, mask_inv = cv2.threshold(gray_canvas, 20, 255, cv2.THRESH_BINARY_INV)
    
    # Wherever you drew, mask_inv cuts out the webcam pixels to create pure solid black ink
    final_output = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Keyboard control actions inside the running loop
    key_input = cv2.waitKey(1) & 0xFF
    if key_input == ord('c'):
        canvas = np.zeros_like(frame)  # Manual erase trigger
        xp, yp = 0, 0
    elif key_input == ord('q'):
        break

    cv2.imshow("High-Performance Black Ink Canvas", final_output)

cap.release()
cv2.destroyAllWindows()
