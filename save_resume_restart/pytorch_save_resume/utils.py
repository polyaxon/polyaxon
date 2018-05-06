from __future__ import division
from __future__ import print_function


import logging

import torch

from polyaxon_helper import get_outputs_path

logging.basicConfig(level=logging.INFO)


def get_weight_filename():
    return '{}/{}'.format(get_outputs_path(), 'checkpoint.pth.tar')


def set_seed(seed, cuda):
    # Seed for reproducibility
    torch.manual_seed(seed)
    if cuda:
        torch.cuda.manual_seed(seed)
