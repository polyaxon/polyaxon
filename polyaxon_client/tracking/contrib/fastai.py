# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.tracking import Experiment

try:
    from fastai.callbacks import TrackerCallback
except ImportError:
    raise PolyaxonClientException('Fastai is required to use PolyaxonFastai')


class PolyaxonFastai(TrackerCallback):

    def __init__(self, learn, experiment=None, monitor='val_loss', mode='auto'):
        super(PolyaxonFastai, self).__init__(learn, monitor=monitor, mode=mode)
        self.experiment = experiment
        if settings.IS_MANAGED:
            self.experiment = self.experiment or Experiment()

    def on_epoch_end(self, epoch, smooth_loss, last_metrics, **kwargs):
        if not self.experiment:
            return
        metrics = {
            name: stat for name, stat in
            list(zip(self.learn.recorder.names, [epoch, smooth_loss] + last_metrics))[1:]
        }

        self.experiment.log_metrics(**metrics)
