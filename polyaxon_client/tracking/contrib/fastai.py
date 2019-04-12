# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.exceptions import PolyaxonClientException

try:
    from fastai.callbacks import TrackerCallback
except ImportError:
    raise PolyaxonClientException('Fastai is required to use PolyaxonFastai')


class PolyaxonFastai(TrackerCallback):

    def __init__(self, learn, experiment, monitor='val_loss', mode='auto'):
        super().__init__(learn, monitor=monitor, mode=mode)
        self.experiment = experiment

    def on_epoch_end(self, epoch, smooth_loss, last_metrics, **kwargs):
        metrics = {
            name: stat for name, stat in
            list(zip(self.learn.recorder.names, [epoch, smooth_loss] + last_metrics))[1:]
        }

        self.experiment.log_metrics(**metrics)
