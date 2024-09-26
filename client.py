import socket
import numpy as np
import keyboard
from mapping import DI
import cv2 
import threading
import queue
import logging 

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s] %(message)s')
# create a queue for thread-safe data sharing
data_queue = queue.Queue()

# receive data from model 
def receive_data():
    recv_s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_host= socket.gethostname()
    recv_port= 12346
    recv_s.connect((recv_host, recv_port))

    while True:
        msg= recv_s.recv(1024)
        if keyboard.is_pressed("esc"):
            break
        if msg:
            raw_data = msg.decode('utf-8')
            # possible_numbers = [raw_data[i:i+18] for i in range(0, len(raw_data), 18)]
            possible_numbers = raw_data.strip().split('\n')

        # Process each float value in the message
            for num_str in possible_numbers:
                try:
                    num = float(num_str)
                    int_value = int(num*100)
                    logging.info(f"received:{num}, processed:{int_value}")  
                    procesed_data = f"{int_value}\n" #apppend a newline character for separation
                    data_queue.put(procesed_data) # put the data into the queue

                #s_esp32.sendall(num.encode('utf-8'))
                #updata_image(num*100)

                except ValueError:
                    logging.info(f"Could not convert {num_str} to float")
                continue

    
            if cv2.waitKey(1)&0xFF== ord('q'):
                break

            #cv2.destroyAllWindows()
    recv_s.close()



#send processed data to esp32
def send_data():

    #setting up the client to send data to esp32
    s_esp32 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_file3 = '192.168.11.22'
    port_file3 = 12347
    s_esp32.connect((host_file3, port_file3))
    logging.info("connected to esp32")

    while True:
        data_for_esp32 = data_queue.get() # get processed data from queue
        #data_for_esp32 = f"{data_test}"
        V_for_esp32 = DI(60, 140, int(data_for_esp32))
        s_esp32.sendall(f"{V_for_esp32}\n".encode('utf-8'))  # here need to convert the float 'v_for_esp32' to a string and then encode it to UTF-8 before sending it
        data_queue.task_done()
        logging.info(f"{V_for_esp32}")
        if keyboard.is_pressed("esc"):
            break
    
    s_esp32.close()

'''
# distance visualization
window_name = 'distance visualization'
width, height = 640, 480
max_distance = 200
history_length = 50

distannce_history = [] # empty list to store value
img = np.zeros((height, width, 3), dtype= np.uint8) # blank image to draw on

def updata_image(distance):
    global distannce_history, img

    distannce_history.append(distance)
    if len(distannce_history) > history_length:
        distannce_history.pop(0)

    img.fill(0)

    for i in range(1, len(distannce_history)):  
        # this loop starts from the second element(index 1) and goes through each element in the 'distance_history' list
        # as we are going to draw a line between the previous point(index'i-1') and the current point(index'i')
        pt1 = (int((i-1)*(width/history_length)), height- int((distannce_history[i-1]/max_distance)*height))
        pt2 = (int(i*(width/history_length)), height-int((distannce_history[i]/ max_distance)*height))
        cv2.line(img, pt1, pt2, (0,255,0), 2)
    
    cv2.imshow(window_name, img)
    cv2.waitKey(1)

cv2.namedWindow(window_name)
'''
'''
while True:
    
    msg= s.recv(1024)
    if keyboard.is_pressed("esc"):
        break

    raw_data = msg.decode('utf-8')
    possible_numbers = [raw_data[i:i+18] for i in range(0, len(raw_data), 18)]

    # Process each float value in the message
    for num_str in possible_numbers:
        try:
            num = float(num_str)
            print(num, num*100)

            #s_esp32.sendall(num.encode('utf-8'))

            #updata_image(num*100)

        except ValueError:
            print(f"Could not convert {num_str} to float")
            continue

    
    if cv2.waitKey(1)&0xFF== ord('q'):
        break

#cv2.destroyAllWindows()
#s.close()
'''
# create and start threads
recv_thread = threading.Thread(target=receive_data, name= 'receiver')
send_thread = threading.Thread(target=send_data, name = 'sender')

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()