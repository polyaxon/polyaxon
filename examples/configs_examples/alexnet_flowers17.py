# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx

from polyaxon.polyaxonfile import local_runner


if __name__ == "__main__":
    """Creates an experiment using Alexnet applied to Oxford's 17  Category Flower Dataset.

    References:
        * Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet Classification with
        Deep Convolutional Neural Networks. NIPS, 2012.
        * 17 Category Flower Dataset. Maria-Elena Nilsback and Andrew Zisserman.

    Links:
        * [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)  # noqa
        * [Flower Dataset (17)](http://www.robots.ox.ac.uk/~vgg/data/flowers/17/)
    """
    plx.datasets.flowers17.prepare('../data/flowers17')
    local_runner.run('./yaml_configs/alexnet_flower17.yml')
