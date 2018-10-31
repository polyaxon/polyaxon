import numpy as np
import torch
from torchvision.transforms import RandomVerticalFlip, RandomHorizontalFlip, RandomCrop
from torchvision.transforms import ColorJitter, ToTensor


class GlobalContrastNormalize(object):
    """
    Code adapted from https://github.com/lisa-lab/pylearn2/blob/master/pylearn2/expr/preprocessing.py#L16
    """

    def __init__(self, scale=1., subtract_mean=True,
                 use_std=False, sqrt_bias=0., min_divisor=1e-8):
        self.scale = scale
        self.subtract_mean = subtract_mean
        self.use_std = use_std
        self.sqrt_bias = sqrt_bias
        self.min_divisor = min_divisor

    def __call__(self, img_tensor):
        if self.subtract_mean:
            mean = torch.mean(img_tensor)
            img_tensor -= mean

        if self.use_std:
            img_var = torch.var(img_tensor)
        else:
            img_var = torch.sum(torch.pow(img_tensor, 2.0))
        normalizer = np.sqrt(self.sqrt_bias + img_var) / self.scale
        normalizer = 1.0 if normalizer < self.min_divisor else normalizer
        return img_tensor / normalizer


train_data_transform = [
    RandomCrop(size=32, padding=4),
    RandomHorizontalFlip(p=0.5),
    RandomVerticalFlip(p=0.5),
    ColorJitter(hue=0.1, brightness=0.1),
    ToTensor(),
    # https://github.com/lisa-lab/pylearn2/blob/master/pylearn2/scripts/datasets/make_cifar10_gcn_whitened.py#L19
    GlobalContrastNormalize(scale=55.0)
]


val_data_transform = [
    RandomHorizontalFlip(p=0.5),
    RandomVerticalFlip(p=0.5),
    ToTensor(),
    # https://github.com/lisa-lab/pylearn2/blob/master/pylearn2/scripts/datasets/make_cifar10_gcn_whitened.py#L58
    GlobalContrastNormalize(scale=55.0)
]

test_data_transform = val_data_transform
