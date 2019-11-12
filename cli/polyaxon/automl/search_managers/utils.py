import numpy as np


def get_random_generator(seed=None):
    return np.random.RandomState(seed) if seed else np.random
