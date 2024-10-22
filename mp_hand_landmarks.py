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

#initialize variables for UKF
ukf = None
ukf_initialized = None
fps = 30  # checked manually
dt = 1/ fps

def initialize_ukf_once(initial_landmarks):
    global ukf, ukf_initialized
    if not ukf_initialized:
        ukf = initialize_ukf(initial_landmarks, dt)
        ukf_initialized = True

def process_frame(image):
    global ukf, ukf_initialized

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
    # Process the image and find hands
    results = hands.process(image_rgb)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            all_transformed_lm, scale_factor = mapping.transform_coordinates(hand_landmarks.landmark)
            print(hand_landmarks)
            selected_lm = all_transformed_lm[INDEX_LMN]
            original_wrist = all_transformed_lm[0]

            print("selected_lm", selected_lm)
            print("\n")
            

            if selected_lm.shape != (5, 3):
                print(f"Warning: selected_lm shape is {selected_lm.shape}, expected (5, 3)")
                print(f"Selected landmarks: {selected_lm}")
                return image_bgr

            if not ukf_initialized:
                initialize_ukf_once(selected_lm)

            if ukf_initialized:
                measurement = selected_lm.flatten()
                refined_landmarks = update_ukf(ukf, measurement)
                detransformed_landmarks = mapping.detransform_coordinates(refined_landmarks, original_wrist, scale_factor)
                print("refined landmarks:", refined_landmarks)
                print("detransformed_landmarks:", detransformed_landmarks)

    
    return image_bgr


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands # here we access a module or a class, dont use()
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

    image = process_frame(image)
    image = cv2.flip(image, 1)

    # Display the image
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()