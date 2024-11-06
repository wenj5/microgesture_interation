import socket
import keyboard

def send_data():
    # set up the client to send sada to esp32
    s_esp32 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_file = '192.168.11.22'
    port_file = 12347
    s_esp32.connect((host_file, port_file))

    return s_esp32


while True:
    data_for_esp32 = 123
    s_esp32 = send_data()
    s_esp32.sendall(f"{data_for_esp32}\n".encode('utf-8'))

    if keyboard.is_pressed("esc"):
        break

s_esp32.close()