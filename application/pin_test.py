from machine import Pin, PWM
import time

# Define motor control pins
# Motor A
IN1 = Pin(13, Pin.OUT)    # G22
IN2 = Pin(14, Pin.OUT)    # G19
ENA = PWM(Pin(32))        # G25 - PWM for speed control

# Motor B
IN3 = Pin(27, Pin.OUT)    # G23
IN4 = Pin(19, Pin.OUT)    # G33
ENB = PWM(Pin(33))        # G21 - PWM for speed control

# Initialize PWM frequency (0-1023)
ENA.freq(10000)    # Set PWM frequency to 1kHz
ENB.freq(10000)

def set_motor_speed(enable_pin, speed):
    """
    Set motor speed (0-100%)
    Args:
        enable_pin: PWM pin object
        speed: Speed percentage (0-100)
    """
    # Convert 0-100 to 0-1023 (PWM range in MicroPython)
    pwm_value = int(speed * 1023 / 100)
    enable_pin.duty(pwm_value)

def motor_forward(speed):
    """Move both motors forward"""
    # Motor A
    IN1.value(1)
    IN2.value(0)
    # Motor B
    IN3.value(0)
    IN4.value(1)
    # Set speed to 50%
    set_motor_speed(ENA, speed)
    set_motor_speed(ENB, speed)

def motor_backward(speed):
    """Move both motors backward"""
    # Motor A
    IN1.value(0)
    IN2.value(1)
    # Motor B
    IN3.value(1)
    IN4.value(0)
    # Set speed to 50%
    set_motor_speed(ENA, speed)
    set_motor_speed(ENB, speed)

def motor_stop():
    """Stop both motors"""
    # Motor A
    IN1.value(0)
    IN2.value(0)
    # Motor B
    IN3.value(0)
    IN4.value(0)
    # Set speed to 0
    set_motor_speed(ENA, 0)
    set_motor_speed(ENB, 0)

# Test the motors
try:
    while True:
        print("Motors forward")
        print("70")
        motor_forward(70)
        time.sleep(2)
        motor_stop()
        
        print("75")
        motor_forward(75)
        time.sleep(2)
        motor_stop()
        
        
        print("80")
        motor_forward(80)
        time.sleep(2)
        motor_stop()
        print("82")
        motor_forward(82)
        time.sleep(2)
        motor_stop()
        print("84")
        motor_forward(84)
        time.sleep(2)
        motor_stop()
        print("86")
        motor_forward(86)
        time.sleep(2)
        motor_stop()
        print("88")
        motor_forward(88)
        time.sleep(2)
        motor_stop()
        print("90")
        motor_forward(90)
        time.sleep(2)
        motor_stop()
        print("95")
        motor_forward(95)
        time.sleep(2)
        motor_stop()
        print("98")
        motor_forward(98)
        time.sleep(2)
        
        
        print("Motors stop")
        motor_stop()
        time.sleep(1)
        
        
except KeyboardInterrupt:
    print("Stopping motors")
    motor_stop()