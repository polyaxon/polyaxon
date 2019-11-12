import numpy as np


def uniform(low, high, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.uniform(low=low, high=high, size=size)


def quniform(low, high, q, size=None, rand_generator=None):
    value = uniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.round(value // q) * q


def loguniform(low, high, size=None, rand_generator=None):
    value = uniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.exp(value)


def qloguniform(low, high, q, size=None, rand_generator=None):
    value = loguniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.round(value // q) * q


def normal(loc, scale, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.normal(loc=loc, scale=scale, size=size)


def qnormal(loc, scale, q, size=None, rand_generator=None):
    draw = normal(loc=loc, scale=scale, size=size, rand_generator=rand_generator)
    return np.round(draw // q) * q


def lognormal(loc, scale, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.lognormal(mean=loc, sigma=scale, size=size)


def qlognormal(loc, scale, q, size=None, rand_generator=None):
    draw = lognormal(loc=loc, scale=scale, size=size, rand_generator=rand_generator)
    return np.round(draw // q) * q
