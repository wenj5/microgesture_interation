import socket


def send_data():
    # set up the client to send sada to esp32
    s_esp32 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_file = '192.168.11.22'
    port_file = 12347
    s_esp32.connect((host_file, port_file))

    return(print("connected to esp32"))