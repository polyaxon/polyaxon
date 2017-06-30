# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from .exploration_decay import (
    exponential_decay,
    piecewise_constant,
    polynomial_decay,
    natural_exp_decay,
    inverse_time_decay
)
from .explorations import (
    EXPLORATIONS,
    constant,
    greedy,
    random,
    decay,
)
