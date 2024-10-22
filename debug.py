import cv2
import mediapipe as mp
import mapping
import numpy as np
from ukf import initialize_ukf, update_ukf
import traceback

INDEX_LMN = [0, 5, 6, 7, 8]
THUMB_LMN = [0, 1, 2, 3, 4]
MIDDLE_LMN = [0, 9, 10, 11, 12]
RING_LMN = [0, 13, 14, 15, 16]
PINKY_LMN = [0, 17, 18, 19, 20]

ukf = None
ukf_initialized = False
fps = 30
dt = 1 / fps

def initialize_ukf_once(initial_landmarks):
    global ukf, ukf_initialized
    if not ukf_initialized:
        try:
            print(f"Initializing UKF with landmarks shape: {initial_landmarks.shape}")
            ukf = initialize_ukf(initial_landmarks, dt)
            ukf_initialized = True
            print("UKF initialized successfully.")
        except Exception as e:
            print(f"Error initializing UKF: {e}")
            print(f"Initial landmarks: {initial_landmarks}")
            traceback.print_exc()

def process_frame(image, frame_count):
    global ukf, ukf_initialized
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
    results = hands.process(image_rgb)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            all_transformed_lm = mapping.transform_coordinates(hand_landmarks.landmark)
            selected_lm = np.array([all_transformed_lm[i] for i in INDEX_LMN])
            # selected_lm = all_transformed_lm[INDEX_LMN]
            
            if selected_lm.shape != (5, 3):
                print(f"Frame {frame_count} - Warning: selected_lm shape is {selected_lm.shape}, expected (5, 3)")
                print(f"Selected landmarks: {selected_lm}")
                return image_bgr

            print(f"Frame {frame_count} - Selected landmarks shape:", selected_lm.shape)

            if not ukf_initialized:
                initialize_ukf_once(selected_lm)
            
            if ukf_initialized:
                try:
                    measurement = selected_lm.flatten()
                    refined_landmarks = update_ukf(ukf, measurement)
                    print(f"Frame {frame_count} - Refined landmarks shape:", refined_landmarks.shape)
                except Exception as e:
                    print(f"Frame {frame_count} - Error updating UKF: {e}")
                    print(f"Measurement shape: {measurement.shape}")
                    print(f"UKF state shape: {ukf.x.shape}")
                    traceback.print_exc()
                    ukf_initialized = False
                    ukf = None
    else:
        print(f"Frame {frame_count} - No hand landmarks detected in this frame.")

    return image_bgr

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

frame_count = 0

try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        frame_count += 1
        print(f"Processing frame {frame_count}")

        image = process_frame(image, frame_count)
        image = cv2.flip(image, 1)
        
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
            break

except Exception as e:
    print(f"An error occurred: {e}")
    print("Traceback:")
    traceback.print_exc()

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Video capture ended.")