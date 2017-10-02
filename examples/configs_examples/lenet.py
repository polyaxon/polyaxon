# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx

from polyaxon.polyaxonfile import local_runner


if __name__ == "__main__":
    """Creates an experiment using Lenet network.

    Links:
        * http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf
    """
    plx.datasets.mnist.prepare('../data/mnist')
    local_runner.run('./yaml_configs/lenet.yml')
