import numpy as np
from filterpy.kalman import UnscentedKalmanFilter as UKF
from filterpy.kalman import MerweScaledSigmaPoints

def initialize_ukf(initial_state, dt):
    # for single finger
    num_landmark = 5
    state_dim = num_landmark* 3 # for (x, y, z)

    initial_state = np.array(initial_state).flatten()
