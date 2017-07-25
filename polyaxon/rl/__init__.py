# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.rl.exploration_decay import (
    exponential_decay,
    piecewise_constant,
    polynomial_decay,
    natural_exp_decay,
    inverse_time_decay
)
from polyaxon.rl.explorations import (
    DISCRETE_EXPLORATIONS,
    CONTINUOUS_EXPLORATIONS,
    constant,
    greedy,
    random,
    decay,
    random_decay,
    ornsteinuhlenbeck_process,
)

from polyaxon.rl import environments
from polyaxon.rl import memories
from polyaxon.rl.utils import (
    get_global_episode,
    get_or_create_global_episode,
    create_global_episode,
    get_global_timestep,
    get_or_create_global_timestep,
    create_global_timestep
)
