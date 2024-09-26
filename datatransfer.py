import socket 
import time
import keyboard


#send processed data to esp32
host_file3 = '192.168.11.6'
port_file3 = 12347

#setting up the client to send data to esp32
s_esp32 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_esp32.connect((host_file3, port_file3))

data_test = 12345678
data_for_esp32 = f"{data_test}"

while True:
    s_esp32.sendall(data_for_esp32.encode('utf-8'))
    if keyboard.is_pressed("esc"):
        break
    print(data_test)


