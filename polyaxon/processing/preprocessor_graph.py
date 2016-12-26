# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class PreprocessorGraph(object):
    """A data preprocessor handler.

    If the preprocessor is used for data augmentation `input_data`,
    then methods will be applied at training time only.
    Otherwise the methods will be applied at both training time and testing time.

    Params:
        for_data_augmentation: `boolean`.
        methods: `list of function`. The augmentation methods to apply.
        kwargs: A `list` of kwargs to use for these methods.
    """

    def __init__(self, for_data_augmentation=False):
        self.for_data_augmentation = for_data_augmentation
        self.methods = []
        self.kwargs = []

    def apply(self, batch):
        for i, m in enumerate(self.methods):
            if self.kwargs[i]:
                batch = m(batch, **self.kwargs[i])
            else:
                batch = m(batch)
        return batch

    def add(self, method, kwargs):
        self.methods.append(method)
        self.kwargs.append(kwargs)
