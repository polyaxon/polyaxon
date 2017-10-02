# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx

from polyaxon.polyaxonfile import local_runner


if __name__ == "__main__":
    """Creates an experiment using cnn for CIFAR-10 dataset classification task.

    References:
        * Learning Multiple Layers of Features from Tiny Images, A. Krizhevsky, 2009.

    Links:
        * [CIFAR-10 Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)
    """
    plx.datasets.cifar10.prepare('../data/cifar10')
    local_runner.run('./yaml_configs/convnet_cifar10.yml')
