# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn
from tensorflow.python.estimator.inputs.pandas_io import pandas_input_fn


from polyaxon.processing.image import IMAGE_PROCESSORS
from polyaxon.processing.categorical import CategoricalVocabulary, CategoricalProcessor
from polyaxon.processing.data_decoders import (
    DataDecoder,
    TFExampleDecoder,
    SplitTokensDecoder,
    TFSequenceExampleDecoder
)
from polyaxon.processing.data_providers import (
    Dataset,
    DataProvider,
    DatasetDataProvider,
    ParallelDatasetProvider
)
from polyaxon.processing import image
from polyaxon.processing.input_data import create_input_data_fn
from polyaxon.processing.text import VocabularyProcessor
from polyaxon.processing import pipelines


PROCESSORS = IMAGE_PROCESSORS
