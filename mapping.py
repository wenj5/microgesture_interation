import numpy as np


class map:
# Vmax here can be any value which is the maximum value been controled - here is velocity
# Dmax here is the maximum distance between target finger
# changing distance between fingers
    def DI(Vmax, Dmax, dtm):
        r = Vmax/Dmax
        if dtm < Dmax:
            v = r*dtm
        else: 
            v = r*Dmax
        return int(v)

# defination of values are the same as above
# indirect mapping

    def IDI(Amax, Dmax, dti):
        r2 = Amax/Dmax
        a = (Dmax-dti)*r2
        return a
    

def transform_coordinates(landmarks):
    '''
    transform hand landmarks to a coordinate system with the wrist as origin
    '''
    landmark_array= np.array([[lm.x, lm.y, lm.z] for lm in landmarks])
    wrist = landmark_array[0]
    transformed_landmarks = landmark_array - wrist
    scale_factor = 1/ (np.max(np.abs(transformed_landmarks)) + 1e-6) #added by 1e-6 to avoid division by zero
    transformed_landmarks *= scale_factor

    return transformed_landmarks


def distance_cal(landmarks, j_id1, j_id2):

    Ttip = (landmarks[j_id1] + landmarks[(j_id1-1)])/ 2
    Itip = (landmarks[j_id2] + landmarks[(j_id2-1)])/ 2
    distance = np.linalg.norm(Ttip - Itip)

    return distance



