#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from polyaxon import tracking
from polyaxon.exceptions import PolyaxonClientException

try:
    from fastai.basics import *
    from fastai.learner import Callback
    from fastai.vision.all import *
except:
    raise PolyaxonClientException("Fastai is required to use PolyaxonFastai")


class PolyaxonFastaiCallback(Callback):
    """Log losses, metrics, model weights, model architecture summary to polyaxon"""

    def __init__(self, log_model=False, run=None):
        self.log_model = log_model
        self.plx_run = tracking.get_or_create_run(run)
        self._plx_step = 0

    def before_fit(self):
        if not self.plx_run:
            return
        try:
            self.plx_run.log_inputs(
                n_epoch=str(self.learn.n_epoch), model_class=str(type(self.learn.model))
            )
        except:
            print("Did not log all properties to Polyaxon.")

        try:
            model_summary_path = "{}/model_summary.txt".format(
                self.plx_run.get_outputs_path()
            )
            with open(model_summary_path, "w") as g:
                g.write(repr(self.learn.model))
            self.plx_run.log_file_ref(path=model_summary_path, name="model_summary")
        except:
            print(
                "Did not log model summary. "
                "Check if your model is PyTorch model and the Polyaxon has correctly initialized "
                "the artifacts/outputs path."
            )

        if self.log_model and not hasattr(self.learn, "save_model"):
            print(
                "Unable to log model to Polyaxon.\n",
                'Use "SaveModelCallback" to save model checkpoints '
                "that will be logged to Polyaxon.",
            )

    def after_batch(self):
        # log loss and opt.hypers
        if self.learn.training:
            self._plx_step += 1
            metrics = {
                "smooth_loss": to_detach(self.smooth_loss.clone()),
                "raw_loss": to_detach(self.loss.clone()),
                "train_iter": self.learn.train_iter,
            }
            for i, h in enumerate(self.learn.opt.hypers):
                for k, v in h.items():
                    metrics[f"hypers_{k}"] = v
            self.plx_run.log_metrics(step=self._plx_step, **metrics)

    def after_epoch(self):
        # log metrics
        self.plx_run.log_metrics(
            step=self._plx_step,
            **{
                n: v
                for n, v in zip(self.recorder.metric_names, self.recorder.log)
                if n not in ["train_loss", "epoch", "time"]
            },
        )

        # log model weights
        if self.log_model and hasattr(self.learn, "save_model"):
            if self.learn.save_model.every_epoch:
                _file = join_path_file(
                    f"{self.learn.save_model.fname}_{self.learn.save_model.epoch}",
                    self.learn.path / self.learn.model_dir,
                    ext=".pth",
                )
            else:
                _file = join_path_file(
                    self.learn.save_model.fname,
                    self.learn.path / self.learn.model_dir,
                    ext=".pth",
                )
            self.plx_run.log_model(_file, framework="fastai", step=self._plx_step)
