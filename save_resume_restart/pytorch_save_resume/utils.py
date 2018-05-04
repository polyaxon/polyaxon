import torch

from polyaxon_helper import get_outputs_path


def get_weight_filename():
    return '{}/{}'.format(get_outputs_path(), 'checkpoint.pth.tar')


def set_seed(seed, cuda):
    # Seed for reproducibility
    torch.manual_seed(seed)
    if cuda:
        torch.cuda.manual_seed(seed)
