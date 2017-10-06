# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow.contrib.learn as tflearn


class CategoricalVocabulary(tflearn.preprocessing.CategoricalVocabulary):
    """Categorical variables vocabulary class.

    Accumulates and provides mapping from classes to indexes.
    Can be easily used for words.
    """
    pass


class CategoricalProcessor(tflearn.preprocessing.CategoricalProcessor):
    """Maps documents to sequences of word ids.

    As a common convention, Nan values are handled as unknown tokens.
    Both float('nan') and np.nan are accepted.
    """
