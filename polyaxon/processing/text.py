# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow.contrib.learn as tflearn


class VocabularyProcessor(tflearn.preprocessing.VocabularyProcessor):
    """A mirror to tf.contrib.learn VocabularyProcessor.

    Maps documents to sequences of word ids.

    Args:
        max_document_length: Maximum length of documents.
            if documents are longer, they will be trimmed, if shorter - padded.
        min_frequency: Minimum frequency of words in the vocabulary.
        vocabulary: CategoricalVocabulary object.

    Attributes:
        vocabulary: CategoricalVocabulary object.
    """
    pass
