import socket
import keyboard
import time
import logging



def find_esp32_ip():
    while True:
        try:
            ip = input("Enter ESP32's IP address: ")
            #check if IP has 4 parts and each is 0-255
            parts = ip.split('.')
            if len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts):
                return ip
            print("Invalid IP format. Example: 192.168.1.22")
        except ValueError:
            print("Please enter a valid IP address")

def connect_to_esp32(host, port, max_retries= 3):
    #Try to connect multiple times
    for attempt in range(max_retries):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            print(f"Connecting to ESP32 at {host}:{port} (Try {attempt + 1}/{max_retries})")
            sock.connect((host, port))
            print("Connected!")
            return sock
            
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying in 2 seconds...")
                time.sleep(2)
    
    return None



def main():
    ESP32_IP = '192.168.11.5'
    ESP32_PORT = 12347
    esp32 = connect_to_esp32(ESP32_IP, ESP32_PORT)
    if not esp32:
        print("Couldn't connect")
        return
    
    try:
        while True:
            try:
                data = 35
                esp32.sendall(f"{data}\n".encode('utf-8'))
                print(f"Sent: {data}")
                
            except socket.error as e:
                print(f"Send failed: {str(e)}")
                break
                
            if keyboard.is_pressed("esc"):
                print("ESC pressed - exiting")
                break 
            # Small delay to prevent CPU overuse
            time.sleep(0.1)
            
    finally:
        if esp32:
            esp32.close()
            print("Connection closed")


'''
if __name__ == "__main__":
    main()
'''
