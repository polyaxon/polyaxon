# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx

from polyaxon.polyaxonfile import local_runner


if __name__ == "__main__":
    """Creates an auto encoder on MNIST handwritten digits.

    inks:
        * [MNIST Dataset] http://yann.lecun.com/exdb/mnist/
    """
    plx.datasets.mnist.prepare('../data/mnist')
    local_runner.run('./yaml_configs/autoencoder_mnist.yml')
