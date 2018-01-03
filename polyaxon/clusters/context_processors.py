# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from clusters.models import Cluster


def cluster(request):
    return {'cluster': Cluster.load()}
