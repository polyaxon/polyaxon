# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow.contrib.learn as tflearn


class CategoricalVocabulary(tflearn.preprocessing.CategoricalVocabulary):
    """Categorical variables vocabulary class.

    Accumulates and provides mapping from classes to indexes.
    Can be easily used for words.
    """

    def __init__(self, unknown_token="<UNK>", support_reverse=True):
        super(CategoricalVocabulary, self).__init__(unknown_token, support_reverse)

    def __len__(self):
        """Returns total count of mappings. Including unknown token."""
        return super(CategoricalVocabulary, self).__len__()

    def freeze(self, freeze=True):
        """Freezes the vocabulary, after which new words return unknown token id.

        Args:
            freeze: True to freeze, False to unfreeze.
        """
        super(CategoricalVocabulary, self).freeze(freeze)

    def get(self, category):
        """Returns word's id in the vocabulary.

        If category is new, creates a new id for it.

        Args:
            category: string or integer to lookup in vocabulary.

        Returns:
            interger, id in the vocabulary.
        """
        return super(CategoricalVocabulary, self).get(category)

    def add(self, category, count=1):
        """Adds count of the category to the frequency table.

        Args:
            category: string or integer, category to add frequency to.
            count: optional integer, how many to add.
        """
        super(CategoricalVocabulary, self).add(category, count)

    def trim(self, min_frequency, max_frequency=-1):
        """Trims vocabulary for minimum frequency.

        Remaps ids from 1..n in sort frequency order.
        where n - number of elements left.

        Args:
            min_frequency: minimum frequency to keep.
            max_frequency: optional, maximum frequency to keep.
                Useful to remove very frequent categories (like stop words).
        """
        super(CategoricalVocabulary, self).trim(min_frequency, max_frequency)

    def reverse(self, class_id):
        """Given class id reverse to original class name.

        Args:
            class_id: Id of the class.

        Returns:
            Class name.

        Raises:
            ValueError: if this vocabulary wasn't initialized with support_reverse.
        """
        return super(CategoricalVocabulary, self).reverse(class_id)


class CategoricalProcessor(tflearn.preprocessing.CategoricalProcessor):
    """Maps documents to sequences of word ids.

    As a common convention, Nan values are handled as unknown tokens.
    Both float('nan') and np.nan are accepted.
    """

    def __init__(self, min_frequency=0, share=False, vocabularies=None):
        """Initializes a CategoricalProcessor instance.

        Args:
            min_frequency: Minimum frequency of categories in the vocabulary.
            share: Share vocabulary between variables.
            vocabularies: list of CategoricalVocabulary objects for each variable in
              the input dataset.

        Attributes:
            vocabularies_: list of CategoricalVocabulary objects.
        """
        super(CategoricalProcessor, self).__init__(min_frequency, share, vocabularies)

    def freeze(self, freeze=True):
        """Freeze or unfreeze all vocabularies.

        Args:
            freeze: Boolean, indicate if vocabularies should be frozen.
        """
        super(CategoricalProcessor, self).freeze(freeze)

    def fit(self, x, unused_y=None):
        """Learn a vocabulary dictionary of all categories in `x`.

        Args:
            x: numpy matrix or iterable of lists/numpy arrays.
               unused_y: to match fit format signature of estimators.

        Returns:
            self
        """
        return super(CategoricalProcessor, self).fit(x, unused_y)

    def fit_transform(self, x, unused_y=None):
        """Learn the vocabulary dictionary and return indexies of categories.

        Args:
            x: numpy matrix or iterable of lists/numpy arrays.
               unused_y: to match fit_transform signature of estimators.

        Returns:
            x: iterable, [n_samples]. Category-id matrix.
        """
        return super(CategoricalProcessor, self).fit_transform(x, unused_y)

    def transform(self, x):
        """Transform documents to category-id matrix.

        Converts categories to ids give fitted vocabulary from `fit` or
        one provided in the constructor.

        Args:
            x: numpy matrix or iterable of lists/numpy arrays.

        Yields:
            x: iterable, [n_samples]. Category-id matrix.
        """
        return super(CategoricalProcessor, self).transform(x)
