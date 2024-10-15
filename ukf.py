import numpy as np
from filterpy.kalman import UnscentedKalmanFilter as UKF
from filterpy.kalman import MerweScaledSigmaPoints

def initialize_ukf(initia_finger_state, dt):
    # for single finger
    num_landmark = 5
    state_dim = num_landmark* 6 # for (x, y, z, x', y', z')

    initial_state = np.array(initia_finger_state).flatten()
    return initial_state


def fx(x, dt):
    F = np.eye(30)
    for i in range(5):
        F[i* 6: i* 6+ 3 , i* 6+ 3: i*6 + 6] = dt *np.eye(3)
    return np.dot(F, x)
