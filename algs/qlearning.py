import numpy

class QLearning:
    def __init__(self, t, r, gamma = 0.9,
                 epsilon = 0.9, epsilon_min = 0.1, epsilon_decay = 0.99,
                 alpha = 0.1, alpha_min = 0.001, alpha_decay = 0.99):
