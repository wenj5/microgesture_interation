import numpy as np

def distance_cal(landmarks, j_id1, j_id2):

    Ttip = (landmarks[j_id1] + landmarks[(j_id1-1)])/ 2
    Itip = (landmarks[j_id2] + landmarks[(j_id2-1)])/ 2
    distance = np.linalg.norm(Ttip - Itip)

    return distance

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
    

