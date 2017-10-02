# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx

from polyaxon.polyaxonfile import local_runner


if __name__ == "__main__":
    """Creates an experiement using a VGG19 to mnist Dataset.

    References:
        * Very Deep Convolutional Networks for Large-Scale Image Recognition.
        K. Simonyan, A. Zisserman. arXiv technical report, 2014.

    Links:
        * http://arxiv.org/pdf/1409.1556
    """
    plx.datasets.mnist.prepare('../data/mnist')
    local_runner.run('./yaml_configs/vgg19.yml')
