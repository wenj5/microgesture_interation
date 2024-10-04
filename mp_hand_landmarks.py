import cv2
import mediapipe as mp
import mapping
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
# Start capturing video from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
    # Process the image and find hands
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the hand landmarks
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            print(hand_landmarks)
            
            # Get landmark positions
            landmarks_m = np.zeros((21, 3))
            for id, lm in enumerate(hand_landmarks.landmark):
                #h, w, c = image.shape
                #cx, cy = int(lm.x * w), int(lm.y * h)
                #cz = lm.z
                landmarks_m[id] = [lm.x, lm.y, lm.z] 
                print(landmarks_m)
                print("\n")
    # Flip the image horizontally for a selfie-view display
    image = cv2.flip(image, 1)

    # Display the image
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()