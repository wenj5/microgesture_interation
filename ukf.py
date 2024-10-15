import numpy as np
from filterpy.kalman import UnscentedKalmanFilter
from filterpy.kalman import MerweScaledSigmaPoints

def initialize_ukf(initial_finger_state, dt):
    # for single finger
    num_landmark = 5
    state_dim = num_landmark* 6 # for (x, y, z, x', y', z')

    initial_state = np.hstack([np.array(initial_finger_state), np.zero((num_landmark, 3))])
    initial_state_flat = np.array(initial_state).flatten()

    # define sigma points
    sigma_p = MerweScaledSigmaPoints(n= state_dim, alpha= 0.1, beta= 2., kappa= -1)
    ukf = UnscentedKalmanFilter(dim_x= state_dim, dim_z= num_landmark* 3, fx= fx, hx= hx, dt= dt, points= sigma_p)
    ukf.x = initial_state_flat
    ukf.P *= 1
    ukf.Q = np.eye(state_dim)* 0.01
    ukf.R = np.eye(num_landmark* 3)* 0.1

    return ukf


# define the state transition function (for 5 landmarks)
def fx(x, dt):
    F = np.eye(len(x))
    for i in range(5):
        F[i* 6: i* 6+ 3 , i* 6+ 3: i*6 + 6] = dt *np.eye(3)
    return np.dot(F, x)

# measurement function
def hx(x):
    return x