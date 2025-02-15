import socket
import cv2
import mediapipe as mp
import mapping
from visualization import Move
import numpy as np
from ukf import initialize_ukf, update_ukf
from s_send import connect_to_esp32, send_data_esp32
import time


INDEX_LMN = [0, 5, 6, 7, 8]
THUMB_LMN = [0, 1, 2, 3, 4]
MIDDLE_LMN = [0, 9, 10, 11, 12]
RING_LMN = [0, 13, 14, 15, 16]
PINKY_LMN = [0, 17, 18, 19, 20]

# Initialize variables for UKF
ukf_thumb = None
ukf_index = None
ukf_middle = None
ukf_ring = None
ukf_thumb_initialized = False
ukf_index_initialized = False
ukf_middle_initialized = False
ukf_ring_initialized = False
fps = 30
dt = 1 / fps

def initialize_ukf_once(initial_landmarks):
    # global ukf, ukf_initialized
    #if not ukf_initialized:
    ukf = initialize_ukf(initial_landmarks, dt)
    return ukf, True

def process_frame(image, esp32):
    global ukf_thumb, ukf_index, ukf_middle, ukf_ring
    global ukf_thumb_initialized, ukf_index_initialized, ukf_middle_initialized, ukf_ring_initialized
    ESP32_IP = '192.168.11.2' # need to change the address everyone wanna connect, address varies
    ESP32_PORT = 12347

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
    results = hands.process(image_rgb)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
   

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            all_transformed_lm, scale_factor = mapping.transform_coordinates(hand_landmarks.landmark)
            index_lm = all_transformed_lm[INDEX_LMN]
            thumb_lm = all_transformed_lm[THUMB_LMN]
            middle_lm = all_transformed_lm[MIDDLE_LMN]
            ring_lm = all_transformed_lm[RING_LMN]
            
            original_wrist = np.array([
                hand_landmarks.landmark[0].x,
                hand_landmarks.landmark[0].y,
                hand_landmarks.landmark[0].z
            ])

            if not ukf_thumb_initialized:
                ukf_thumb, ukf_thumb_initialized = initialize_ukf_once(thumb_lm)

            if not ukf_index_initialized:
                ukf_index, ukf_index_initialized = initialize_ukf_once(index_lm)
            
            if not ukf_middle_initialized:
                ukf_middle, ukf_middle_initialized = initialize_ukf_once(middle_lm)

            if not ukf_ring_initialized:
                ukf_ring, ukf_ring_initialized = initialize_ukf_once(ring_lm)

            if ukf_thumb_initialized and ukf_index_initialized:
                # refine the landmarks of fingers
                thumb_measurement = thumb_lm.flatten()
                refined_thumb = update_ukf(ukf_thumb, thumb_measurement)
                #print(refined_thumb, "in shape of: ", refined_thumb.shape)
                #print(refined_thumb[4])
                # detransformed lanmarks only for drawing
                thumb_landmarks = mapping.detransform_coordinates(
                    refined_thumb, original_wrist, scale_factor
                )
                
                index_measurement = index_lm.flatten()
                refined_index = update_ukf(ukf_index, index_measurement)
                #print(refined_index, "in shape of:", refined_index.shape)
                #print(refined_index[4])
                
                
                middle_measurement = middle_lm.flatten()
                refined_middle = update_ukf(ukf_middle, middle_measurement)
                middle_landmarks = mapping.detransform_coordinates(
                    refined_middle, original_wrist, scale_factor
                )
                
                ring_measurement = ring_lm.flatten()
                refined_ring = update_ukf(ukf_ring, ring_measurement)
                
                # distance calculation and sending data to esp32, get the landmark of tips first
                thumb_np = np.array(refined_thumb[4])
                index_np = np.array(refined_index[4])
                middle_np = np.array(refined_middle[4])
                ring_np = np.array(refined_ring[4])
                distance_1 = int(np.linalg.norm(thumb_np - middle_np)*10)
                distance_0 = int(np.linalg.norm(thumb_np - index_np)*10)
                distance_2 = int(np.linalg.norm(thumb_np - ring_np)*10)
                distance_3 = int(np.linalg.norm(index_np - ring_np)*10)
                # print(thumb_np, middle_np, distance_0)
                try:
                    if esp32:
                        if not send_data_esp32(esp32, [distance_0, distance_1, distance_2, distance_3]):
                            print("attempting to reconnect... ")
                            new_esp32 = connect_to_esp32(ESP32_IP, ESP32_PORT)
                            if new_esp32:
                                esp32 = new_esp32
                                send_data_esp32(esp32, [distance_0, distance_1, distance_2, distance_3])

                        distances = f"{distance_0}, {distance_1}, {distance_2}, {distance_3}\n"
                        # data_to_send = f"{distance_0}\n"
                        esp32.sendall(distances.encode('utf-8'))
                        print(f"send distance: {distances}")
                        time.sleep(0.05)

                        esp32.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

                    # visualizer.updata_image(distance_0)
                    
                except socket.error as e:
                    print(f"failed to send data: {e}")
                    return image_bgr

                # distance visualizing interface drawing x*y = 640* 480
                x_base_0 = 560  # 640 -80
                y_base_0 = 460   # 480 - 20
                gap = 20

                cv2.line(image_bgr, (x_base_0-10, y_base_0-24), (x_base_0+ gap*2+10, y_base_0-24), (82, 23, 68), 2)
                cv2.line(image_bgr, (x_base_0, y_base_0), (x_base_0, 480), (51, 24, 27), 5)
                cv2.line(image_bgr, (x_base_0+ gap, y_base_0), (x_base_0+ gap, 480), (51, 24, 27), 5)
                cv2.line(image_bgr, (x_base_0+ gap*2, y_base_0), (x_base_0+ gap*2, 480), (51, 24, 27), 5)

                cv2.line(image_bgr, (x_base_0+ gap*2, y_base_0+1), (x_base_0+ gap*2, max(y_base_0-distance_0*8, 380)), (89, 68, 171), 3)
                cv2.line(image_bgr, (x_base_0+ gap, y_base_0), (x_base_0+ gap, max(y_base_0- distance_1*8, 380)), (89, 68, 171), 3)
                cv2.line(image_bgr, (x_base_0, y_base_0), (x_base_0, max(y_base_0- distance_2*8, 380)), (89, 68, 171), 3)
                if distance_3 == 0:
                    cv2.rectangle(image_bgr, (x_base_0, 373), (x_base_0+ gap*2, 368), (88, 159, 242), 3)


 
                # Draw original landmarks in blue
                for i in range(len(MIDDLE_LMN)):
                    lm = hand_landmarks.landmark[MIDDLE_LMN[i]]
                    x = int(lm.x * image.shape[1])
                    y = int(lm.y * image.shape[0])
                    cv2.circle(image_bgr, (x, y), 5, (255, 0, 0), -1) 

                    lm = hand_landmarks.landmark[THUMB_LMN[i]]
                    x = int(lm.x * image.shape[1])
                    y = int(lm.y * image.shape[0])
                    cv2.circle(image_bgr, (x, y), 5, (255, 0, 0), -1)
                    


                # Draw refined landmarks in green
                for i, lm in enumerate(thumb_landmarks):
                    x_t = int(lm.x * image.shape[1])
                    y_t = int(lm.y * image.shape[0])
                    cv2.circle(image_bgr, (x_t, y_t), 5, (0, 255, 0), -1)  
                    cv2.putText(image_bgr, f"T{i}", (x_t+10, y_t+10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                for i, lm in enumerate(middle_landmarks):
                    x_i = int(lm.x * image.shape[1])
                    y_i = int(lm.y * image.shape[0])
                    cv2.circle(image_bgr, (x_i, y_i), 5, (0, 255, 0), -1)
                    cv2.putText(image_bgr, f"M{i}", (x_i+10, y_i+10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image_bgr, esp32


def main():
    ESP32_IP = '192.168.11.2' # need to change the address everyone wanna connect, address varies
    ESP32_PORT = 12347
    esp32 = connect_to_esp32(ESP32_IP, ESP32_PORT)
    if not esp32:
        print("Couldn't connect")
        return
    
    # vlz for distance
    # visualizer = Vlz()
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue
            
            image, esp32 = process_frame(image, esp32)
            image = cv2.flip(image, 1)
            cv2.imshow('hand', image)

            if cv2.waitKey(5) & 0xFF == 27:
                print("esc pressed - exiting")
                break

            time.sleep(0.01)

    except Exception as e:
        print(f"Error in main loop: {e}")
        
    finally:
        print("clean up")
        if esp32:
            esp32.close()
            print("esp32 connection cloesd")
        cap.release()
        cv2.destroyAllWindows()
        # visualizer.close_window()

if __name__ == "__main__":
# Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    #ESP32_IP = '192.168.11.18' # need to change the address everyone wanna connect, address varies
    #ESP32_PORT = 12347
    main()

    



