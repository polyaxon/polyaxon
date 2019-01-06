# Code is adapted from https://github.com/Cadene/pretrained-models.pytorch/blob/master/pretrainedmodels/models/nasnet_mobile.py
import torch
import torch.nn as nn

from pretrainedmodels.models.nasnet_mobile import NASNetAMobile


class SmallNASNetAMobile(NASNetAMobile):

    def __init__(self, num_classes, stem_filters=32, penultimate_filters=1056, filters_multiplier=2):
        super(SmallNASNetAMobile, self).__init__(num_classes, stem_filters=stem_filters,
                                                 penultimate_filters=penultimate_filters,
                                                 filters_multiplier=filters_multiplier)
        self.avg_pool = nn.AdaptiveAvgPool2d(1)

    def logits(self, features):
        x = self.relu(features)
        x = self.avg_pool(x)
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        x = self.last_linear(x)
        return x

    def forward(self, input):
        x = self.features(input)
        x = self.logits(x)
        return x
