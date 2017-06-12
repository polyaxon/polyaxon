# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.models.base import BaseModel
from polyaxon.models.generators import Generator
from polyaxon.models.classifiers import Classifier
from polyaxon.models.regressors import Regressor

MODELS = {
    'Classifier': Classifier,
    'Regressor': Regressor,
    'Generator': Generator
}
