import random
import numpy as np
from _mdp_base import Mdp

ACTION = {"LEFT": 0, "DOWN": 1, "RIGHT": 2, "UP": 3}


class FrozenLake(Mdp):
    def __init__(self, size: int = 4, slip_p=[(1.0 / 3.0), (1.0 / 3.0), (1.0 / 3.0)],
                 hole_p: float = 0.2, goal_r: float = 1.0, hole_r: float = 0.0, seed: int = None):
        """
        :param size: The size of the gridworld (Grid = size * size)
        :param slip_p: Slip probability of actions.  Format is [Intended Action, Left, Right]
        :param hole_p: The probability of hole occurrences within the gridworld.
        :param goal_r: The reward for reaching the goal state.
        :param hole_r: The reward for entering a hole state. (CURRENTLY NOT USED)
        :param seed: Used for random number generation
        """
        # Seed the environment
        if seed is not None:
            np.random.seed(seed)

        # Initialize the base class
        super().__init__(size ** 2, 4)

        # Generate the map
        self.world = self._generate_map(size, hole_p)

        # Initialize the shapes for P and R
        self.P = np.zeros((self.num_a, self.num_s, self.num_s))
        self.R = np.zeros((self.num_a, self.num_s, self.num_s))

        # Generate P and R
        self._generate_p_matrix(size=size, slip_p=slip_p, world=self.world)
        self._generate_r_matrix(goal_r=goal_r, hole_r=hole_r)

    def start(self):
        pass

    def next(self, a):
        s_prime = 0
        reward = 0
        return s_prime, reward

    def _generate_map(self, size, hole_p):
        fl_map = np.asarray(['F'] * (size ** 2))
        fl_map[np.random.choice(size ** 2, round((size ** 2) * hole_p))] = 'H'
        fl_map[-1] = 'G'
        # Temporary to help try and ensure there is a path to the goal
        fl_map[1] = 'F'
        fl_map[-2] = 'F'
        return fl_map

    def _generate_p_matrix(self, **kwargs):
        """ The probability matrix is formatted as (A, S, S') such that if you take action A from state S, you will end
        up in state S' with the specified probability"""
        sz = kwargs['size']  # The size of the side of the gridworld
        sz_t = self.num_s  # The total number of state (sz**2)

        for x in range(0, sz_t):
            # *** PROCESS THE 'UP' ACTION (Intended and perpendicular to left/right) ****
            self.P[ACTION['UP'], x, (x - sz) if (x - sz) >= 0 else x] += kwargs['slip_p'][0]
            self.P[ACTION['UP'], x, (x - 1) if x % sz != 0 else x] += kwargs['slip_p'][1]
            self.P[ACTION['UP'], x, (x + 1) if x % sz != sz - 1 else x] += kwargs['slip_p'][2]

            # *** PROCESS THE 'DOWN' ACTION (Intended and perpendicular to left/right) ****
            self.P[ACTION['DOWN'], x, (x + sz) if (x + sz) < sz_t else x] += kwargs['slip_p'][0]
            self.P[ACTION['DOWN'], x, (x + 1) if x % sz != sz - 1 else x] += kwargs['slip_p'][1]
            self.P[ACTION['DOWN'], x, (x - 1) if x % sz != 0 else x] += kwargs['slip_p'][2]

            # *** PROCESS THE 'LEFT' ACTION (Intended and perpendicular to left/right) ****
            self.P[ACTION['LEFT'], x, (x - 1) if x % sz != 0 else x] += kwargs['slip_p'][0]
            self.P[ACTION['LEFT'], x, (x + sz) if (x + sz) < sz_t else x] += kwargs['slip_p'][1]
            self.P[ACTION['LEFT'], x, (x - sz) if (x - sz) >= 0 else x] += kwargs['slip_p'][2]

            # *** PROCESS THE 'RIGHT' ACTION (Intended and perpendicular to left/right) ****
            self.P[ACTION['RIGHT'], x, (x + 1) if x % sz != sz - 1 else x] += kwargs['slip_p'][0]
            self.P[ACTION['RIGHT'], x, (x - sz) if (x - sz) >= 0 else x] += kwargs['slip_p'][1]
            self.P[ACTION['RIGHT'], x, (x + sz) if (x + sz) < sz_t else x] += kwargs['slip_p'][2]

        # Adjust probabilities for where the holes are in the map (if you are in a hole, there
        # is a 1.0 probability you are remaining in it). Same with the goal state
        #policy_char = np.where(map_char == 'H', 'H', policy_char)
        pass



    def _generate_r_matrix(self, **kwargs):
        """ The probability matrix is formatted as (A, S, S') such that if you take action A from state S, you will end
        get the specified reward upon entering state S'"""
        self.R = np.zeros((4, self.num_s, self.num_s))
        self.R[:, :-1, -1] = kwargs["goal_r"]
        pass


if __name__ == "__main__":
    env = FrozenLake()
    pass
