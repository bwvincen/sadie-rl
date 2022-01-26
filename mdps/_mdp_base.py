from abc import ABC, abstractmethod


class Mdp(ABC):
    def __init__(self, num_s: int, num_a: int):
        assert num_s != 0
        assert num_a != 0
        self.num_s = num_s
        self.num_a = num_a
        self.P = None
        self.R = None

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def next(self, a):
        raise NotImplementedError

    @abstractmethod
    def _generate_p_matrix(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def _generate_r_matrix(self, **kwargs):
        raise NotImplementedError
