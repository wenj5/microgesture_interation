from machine import Pin, PWM
import network
import socket
import time
#from motorctrl import motorctrl_init
from dcmotor import DCmotor


def extract_distances(data):
    try:
        distances = [float(x.strip()) for x in data.split(',')]
        if len(distances) == 4:
            return distances
    except:
        return None
    return None

# wifi setup
ssid = 'ifdl'
password = 'hogeupip5'

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(1)
wlan.active(True)
available_networks = wlan.scan()
for network in available_networks:
    print(f"available network:{network}")

wlan.connect(ssid, password)
max_wait = 10
start_time = time.time()

while not wlan.isconnected():
    if time.time() - start_time >= max_wait:
        print("failed to connect to wifi")
        break
    print("trying to connect")
    time.sleep(1)

if wlan.isconnected():
    print('connected to wifi')
    ip = wlan.ifconfig()[0]
    print('IP:', ip)
else:
    print("faild to connect within the timeout period")
    
s_esp32 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# allow reuse the local addr, prep for the reconnection 
s_esp32.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
host = ip
port = 12347
s_esp32.bind((host, port))
s_esp32.listen(1)
# c, addr = s_esp32.accept()
# print('connected by', addr)


# pins for motor setup
frequency = 10000
pin_a1 = Pin(13, Pin.OUT)
pin_a2 = Pin(14, Pin.OUT)
pin_b1 = Pin(27, Pin.OUT)
pin_b2 = Pin(19, Pin.OUT)
enable_a = PWM(Pin(32), frequency)
enable_b = PWM(Pin(33), frequency)
dc_motor = DCmotor(pin_a1, pin_a2, pin_b1, pin_b2, enable_a, enable_b)
dc_motor.stop()


# control constants
DISTANCE_THRESHOULD = 3.0
MAX_DISTANCE = 10.0
MAX_MOTOR_SPEED = 98
MIN_MOTOR_SPEED = 86



while True:
    print("waiting for connection...")
    c = None
    try:
        c, addr = s_esp32.accept()
        print('connected by', addr)
        buffer = ""
        while True:
            try:
                msg = c.recv(256)
                if not msg:
                    print("connection closed by client")
                    break
                
                buffer += msg.decode('utf-8')
                
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    distances = extract_distances(line)
                    
                    if distances:
                        thumb_index_d, thumb_middle_d, thumb_ring_d, index_ring_d = distances # distance relocate
                        print(f"{thumb_index_d}, {thumb_middle_d}, {thumb_ring_d}, {index_ring_d}")
                        if index_ring_d == 0:
                            dc_motor.backward(86)
                        else:
                            if thumb_middle_d > DISTANCE_THRESHOULD: # forward
                            # distance 4-10 maps to speed 86-98
                                speed = min(((thumb_middle_d - (DISTANCE_THRESHOULD+1))* 2 + MIN_MOTOR_SPEED), MAX_MOTOR_SPEED)
                                if thumb_index_d <= (DISTANCE_THRESHOULD - 1) and thumb_ring_d > DISTANCE_THRESHOULD :
                                    dc_motor.forward_right(speed)
                                elif thumb_index_d > DISTANCE_THRESHOULD  and  thumb_ring_d <= (DISTANCE_THRESHOULD - 1):
                                    dc_motor.forward_left(speed)
                                else:
                                    dc_motor.forward(speed)

                            elif thumb_index_d <= DISTANCE_THRESHOULD  and thumb_ring_d > DISTANCE_THRESHOULD :
                                dc_motor.right_only(96)
                            elif thumb_index_d > DISTANCE_THRESHOULD and thumb_ring_d <= DISTANCE_THRESHOULD :
                                dc_motor.left_only(96)
                            else:
                                dc_motor.stop()
                                
  
            except OSError as e:
                print(f"connection error: {e}")
                dc_motor.stop()
                continue
            
            except Exception as e:
                print(f"Error processing data: {e}")
                dc_motor.stop()
                break
            
    except Exception as e:
        print(f"connection error: {e}")
            
    finally:
        if c:
            c.close()
        
        dc_motor.stop()
        print("connection closed, restarting... ")
        buffer = "" # clear buffer for new connection
                


    


