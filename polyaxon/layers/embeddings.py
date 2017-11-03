# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

try:
    from tensorflow.python.keras._impl.keras.layers import embeddings
except ImportError:
    from tensorflow.contrib.keras.python.keras.layers import embeddings

from polyaxon_schemas.layers.embeddings import EmbeddingConfig

from polyaxon.libs import getters
from polyaxon.libs.base_object import BaseObject


class Embedding(BaseObject, embeddings.Embedding):
    CONFIG = EmbeddingConfig
    __doc__ = EmbeddingConfig.__doc__

    def __init__(self,
                 input_dim,
                 output_dim,
                 embeddings_initializer='uniform',
                 embeddings_regularizer=None,
                 activity_regularizer=None,
                 embeddings_constraint=None,
                 mask_zero=False,
                 input_length=None,
                 **kwargs):
        super(Embedding, self).__init__(
            input_dim=input_dim,
            output_dim=output_dim,
            embeddings_initializer=getters.get_initializer(embeddings_initializer),
            embeddings_regularizer=getters.get_regularizer(embeddings_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            embeddings_constraint=getters.get_constraint(embeddings_constraint),
            mask_zero=mask_zero,
            input_length=input_length,
            **kwargs)


EMBEDDING_LAYERS = OrderedDict([(Embedding.CONFIG.IDENTIFIER, Embedding)])
