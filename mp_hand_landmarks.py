import cv2
import mediapipe as mp
import mapping
import numpy as np
from ukf import initialize_ukf, update_ukf

INDEX_LMN = [0, 5, 6, 7, 8]
THUMB_LMN = [0, 1, 2, 3, 4]
MIDDLE_LMN = [0, 9, 10, 11, 12]
RING_LMN = [0, 13, 14, 15, 16]
PINKY_LMN = [0, 17, 18, 19, 20]

# Initialize variables for UKF
ukf = None
ukf_initialized = False
fps = 30
dt = 1 / fps

def initialize_ukf_once(initial_landmarks):
    global ukf, ukf_initialized
    if not ukf_initialized:
        ukf = initialize_ukf(initial_landmarks, dt)
        ukf_initialized = True

def process_frame(image):
    global ukf, ukf_initialized
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
    results = hands.process(image_rgb)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            all_transformed_lm, scale_factor = mapping.transform_coordinates(hand_landmarks.landmark)
            selected_lm = all_transformed_lm[INDEX_LMN]
            
            original_wrist = np.array([
                hand_landmarks.landmark[0].x,
                hand_landmarks.landmark[0].y,
                hand_landmarks.landmark[0].z
            ])

            if not ukf_initialized:
                initialize_ukf_once(selected_lm)

            if ukf_initialized:
                measurement = selected_lm.flatten()
                refined_landmarks = update_ukf(ukf, measurement)
                detransformed_landmarks = mapping.detransform_coordinates(
                    refined_landmarks, original_wrist, scale_factor)
                

                # Draw original landmarks in blue
                for i in range(len(INDEX_LMN)):
                    lm = hand_landmarks.landmark[INDEX_LMN[i]]
                    x = int(lm.x * image.shape[1])
                    y = int(lm.y * image.shape[0])
                    cv2.circle(image_bgr, (x, y), 5, (255, 0, 0), -1) 
                    

                # Draw refined landmarks in green
                for i, lm in enumerate(detransformed_landmarks):
                    x = int(lm.x * image.shape[1])
                    y = int(lm.y * image.shape[0])
                    cv2.circle(image_bgr, (x, y), 5, (0, 255, 0), -1)  
                    cv2.putText(image_bgr, f"R{i}", (x+10, y+10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image_bgr

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)


while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = process_frame(image)
    image = cv2.flip(image, 1)
    cv2.imshow('MediaPipe Hands', image)
    
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()