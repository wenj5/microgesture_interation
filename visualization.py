import cv2
import numpy as np


class Vlz:
    def __init__(self,w_name = 'visualz', width = 640, height = 480, max_distance = 200, history_length = 50):
        self.window_name = w_name
        self.width = width
        self.height = height
        self.max_distance = max_distance
        self.history_length = history_length
        self.distance_history = []
        self.img = np.zeros((height, width, 3), dtype= np.uint8) # blank image to draw on

        cv2.nameWindow(self.window_name)

    def updata_image(self, distance, distance_history, history_length):
        # global self.distance_history
        distance_history = self.distance_history.append(distance)
         
        if len(distance_history) > history_length:
            history_length.pop(0)

        self.img.fill(0) # fill the array with a single scalar value, which is applied to all elements of the array.

        # draw the distance history as a line graph
        for i in range(1, len(self.distance_history)):
            pt1 = (int((i-1)* (self.width / self.history_length)), 
                   self.height - int((self.max_distance_history[i - 1] / self.max_distance)* self.height))
            pt2 = (int(i* (self.width / self.history_length)),
                   self.height - int((self.distance_history[i] / self.max_distance)* self.height))
            cv2.imshow(self.img, pt1, pt2, (0, 255, 0), 2)
            


        
             


# is self.value the global value in a class? 

