import cv2
import numpy as np


class Vlz:
    def __init__(self, width = 640, height = 480, max_distance = 200, history_length = 50):
        self.width = width
        self.height = height
        self.max_distance = max_distance
        self.history_length = history_length
        self.distance_history = []
        self.img = np.zeros((height, width, 3), dtype= np.uint8) # blank image to draw on

    def updata_image(distance, distance_history, history_length):
        # global self.distance_history
         distance_history = self.distance_history.append(distance)
         
         if len(distance_history) > history_length:
             


# is self.value the global value in a class? 

