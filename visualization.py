import cv2
import numpy as np
import time


class Vlz:
    def __init__(self, w_name = 'visualz', width = 640, height = 480, max_distance = 200, history_length = 50):
        self.window_name = w_name
        self.width = width
        self.height = height
        self.max_distance = max_distance
        self.history_length = history_length
        self.distance_history = []
        self.img = np.zeros((height, width, 3), dtype= np.uint8) # blank image to draw on

        cv2.namedWindow(self.window_name)

    def updata_image(self, distance):
        # global self.distance_history
        distance_history = self.distance_history.append(distance)
         
        if len(self.distance_history) > self.history_length:
            self.distance_history.pop(0)

        self.img.fill(0) # fill the array with a single scalar value, which is applied to all elements of the array.

        # draw the distance history as a line graph
        for i in range(1, len(self.distance_history)):
            pt1 = (int((i-1)* (self.width / self.history_length)), 
                   self.height - int((self.distance_history[i - 1] / self.max_distance)* self.height))
            pt2 = (int(i* (self.width / self.history_length)),
                   self.height - int((self.distance_history[i] / self.max_distance)* self.height))
            cv2.line(self.img, pt1, pt2, (0, 255, 0), 2)

        cv2.imshow(self.window_name, self.img)
        cv2.waitKey(1)

    def close_window(self):
        # destroy the window when done
        cv2.destroyWindow(self.window_name)


# test code
visualizer = Vlz()
for i in range(100):
    distance_test = np.random.randint(0, 200)
    visualizer.updata_image(distance_test)
    time.sleep(0.1)

visualizer.close_window()
        
             




