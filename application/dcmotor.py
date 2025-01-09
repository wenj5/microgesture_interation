from machine import Pin, PWM
from time import sleep

class DCmotor:
    def __init__(self, pin_a1, pin_a2, pin_b1, pin_b2, enable_pin_a, enable_pin_b, min_duty=0, max_duty=1023):
        self.pin_a1 = pin_a1
        self.pin_a2 = pin_a2
        self.pin_b1 = pin_b1
        self.pin_b2 = pin_b2
        self.enable_pin_a = enable_pin_a
        self.enable_pin_b = enable_pin_b
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.speed = 0
        #self.speed_factor = 0.2
        
    #speed value is between 0 to 100
    def duty_cycle(self, speed):
        speed = max(0, min(100, speed))
        # reduced_s = speed * self.speed_factor
        if speed <= 0:
            return 0
        else:
            duty_cycle = int(speed * self.max_duty/ 100)
        return max(self.min_duty, min(duty_cycle, self.max_duty))
    
    def forward(self, speed):
        self.speed = speed
        self.enable_pin_a.duty(self.duty_cycle(self.speed))
        self.enable_pin_b.duty(self.duty_cycle(self.speed))
        self.pin_a1.value(0)
        self.pin_a2.value(1)
        self.pin_b1.value(1)
        self.pin_b2.value(0)
        
    def backward(self, speed):
        self.speed = speed
        self.enable_pin_a.duty(self.duty_cycle(self.speed))
        self.enable_pin_b.duty(self.duty_cycle(self.speed))
        self.pin_a1.value(1)
        self.pin_a2.value(0)
        self.pin_b1.value(0)
        self.pin_b2.value(1)
        
    def stop(self):
        self.speed = 0
        self.enable_pin_a.duty(0)
        self.enable_pin_b.duty(0)
        self.pin_a1.value(0)
        self.pin_a2.value(0)
        self.pin_b1.value(0)
        self.pin_b2.value(0)
        
    def right_only(self, speed):
        self.speed = speed
        self.enable_pin_a.duty(0)
        self.enable_pin_b.duty(self.duty_cycle(self.speed))
        self.pin_a1.value(0)
        self.pin_a2.value(0)
        self.pin_b1.value(1)
        self.pin_b2.value(0)
    
    def left_only(self, speed):
        self.speed = speed
        self.enable_pin_a.duty(self.duty_cycle(self.speed))
        self.enable_pin_b.duty(0)
        self.pin_a1.value(0)
        self.pin_a2.value(1)
        self.pin_b1.value(0)
        self.pin_b2.value(0)
        
    def forward_right(self, speed):
        self.speed = speed
        s = speed - 20
        self.enable_pin_a.duty(self.duty_cycle(s))
        self.enable_pin_b.duty(self.duty_cycle(self.speed))
        self.pin_a1.value(0)
        self.pin_a2.value(1)
        self.pin_b1.value(1)
        self.pin_b2.value(0)
    
    def forward_left(self, speed):
        self.speed = speed
        s = speed - 20
        self.enable_pin_a.duty(self.duty_cycle(self.speed))
        self.enable_pin_b.duty(self.duty_cycle(s))
        self.pin_a1.value(0)
        self.pin_a2.value(1)
        self.pin_b1.value(1)
        self.pin_b2.value(0)
        
        
