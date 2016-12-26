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

    def __init__(self,
                 max_document_length,
                 min_frequency=0,
                 vocabulary=None,
                 tokenizer_fn=None):
        super().__init__(max_document_length, min_frequency, vocabulary, tokenizer_fn)

    def fit(self, raw_documents, unused_y=None):
        """ fit.

        Learn a vocabulary dictionary of all tokens in the raw documents.

        Args:
            raw_documents: An iterable which yield either str or unicode.
            unused_y: to match fit format signature of estimators.

        Returns:
            self
        """
        return super().fit(raw_documents, unused_y)

    def fit_transform(self, raw_documents, unused_y=None):
        """ fit_transform.

        Learn the vocabulary dictionary and return indexies of words.

        Args:
            raw_documents: An iterable which yield either str or unicode.
            unused_y: to match fit_transform signature of estimators.

        Returns:
            X: iterable, [n_samples, max_document_length] Word-id matrix.
        """
        return super().fit_transform(raw_documents, unused_y)

    def transform(self, raw_documents):
        """ transform.

        Transform documents to word-id matrix.

        Convert words to ids with vocabulary fitted with fit or the one
        provided in the constructor.

        Args:
            raw_documents: An iterable which yield either str or unicode.

        Yields:
            X: iterable, [n_samples, max_document_length] Word-id matrix.
        """
        return super().transform(raw_documents)

    def reverse(self, documents):
        """ reverse.

        Reverses output of vocabulary mapping to words.

        Args:
            documents: iterable, list of class ids.

        Returns:
            Iterator over mapped in words documents.
        """
        return super().reverse(documents)

    def save(self, filename):
        """ save.

        Saves vocabulary processor into given file.

        Args:
            filename: Path to output file.
        """
        super().save(filename)

    @classmethod
    def restore(cls, filename):
        """ restore.

        Restores vocabulary processor from given file.

        Args:
            filename: Path to file to load from.

        Returns:
            VocabularyProcessor object.
        """
        return super(VocabularyProcessor, cls).restore(filename)
