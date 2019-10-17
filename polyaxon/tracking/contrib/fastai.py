# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon import settings
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.tracking import Run

try:
    from fastai.callbacks import TrackerCallback
except ImportError:
    raise PolyaxonClientException("Fastai is required to use PolyaxonFastai")


class PolyaxonFastai(TrackerCallback):
    def __init__(self, learn, run=None, monitor="val_loss", mode="auto"):
        super(PolyaxonFastai, self).__init__(learn, monitor=monitor, mode=mode)
        self.run = run
        if settings.CLIENT_CONFIG.is_managed:
            self.run = self.run or Run()

    def on_epoch_end(self, epoch, smooth_loss, last_metrics, **kwargs):
        if not self.experiment:
            return
        metrics = {
            name: stat
            for name, stat in list(
                zip(self.learn.recorder.names, [epoch, smooth_loss] + last_metrics)
            )[1:]
        }

        self.run.log_metrics(**metrics)
