# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from polyaxon.estimators.estimator import Estimator
from polyaxon.estimators.agents import Agent
from polyaxon.estimators.hooks import HOOKS


ESTIMATORS = OrderedDict([
    ('Estimator', Estimator),
])

AGENTS = OrderedDict([
    ('Agent', Agent),
])
