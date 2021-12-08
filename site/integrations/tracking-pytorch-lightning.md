---
title: "Pytorch-Lightning Tracking"
meta_title: "Pytorch-Lightning Tracking"
meta_description: "Polyaxon allows to schedule Pytorch-Lightning experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "PyTorch Lightning is an open-source Python library that provides a high-level interface for PyTorch, a popular deep learning framework."
image: "../../content/images/integrations/pytorch-lightning.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - tracking
featured: false
popularity: 2
visibility: public
status: published
---

Polyaxon allows to schedule Pytorch-Lightning experiments and supports tracking metrics, outputs, and models.

With Polyaxon you can:

 * log hyperparameters for every run
 * see learning curves for losses and metrics during training
 * see hardware consumption and stdout/stderr output during training
 * log images, charts, and other assets
 * log git commit information
 * log env information
 * log model
 * ...

## Tracking API

Polyaxon provides a [tracking API](/docs/experimentation/tracking/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard.

You can use the tracking API to create a custom tracking experience with Pytorch-Lightning.

## Setup

In order to use Polyaxon tracking with Pytorch-Lightning, you need to install Polyaxon library

```bash
pip install polyaxon
```

## Initialize your script with Polyaxon

This is an optional step if you need to perform some manual tracking or to track some information before passing the callback.

```python
from polyaxon import tracking

tracking.init(...)
```

## Polyaxon callback

Pass Polyaxon's callback to your logger

```python
from polyaxon.tracking.contrib.pytorch_lightning import PolyaxonCallback

trainer = pl.Trainer(
    gpus=0,
    progress_bar_refresh_rate=20,
    max_epochs=2,
    logger=PolyaxonCallback(),
)
```

## Customizing the callback

Creating the callback will use the current initialized run, but you can use a different run if you need to have more control, the PL callback accepts all `tracking.init` arguments:

```python
from polyaxon.tracking.contrib.pytorch_lightning import PolyaxonCallback

trainer = pl.Trainer(
    gpus=0,
    progress_bar_refresh_rate=20,
    max_epochs=2,
    logger=PolyaxonCallback(
        project="project-name", 
        name="test",
        run_uuid="UUID",
        ...
    ),
)
```

## Manual logging

If you want to have more control and use Polyaxon to log metrics in your scripts, you just need to add `tracking.log_...` anywhere needed:

 * log metrics

```python
tracking.log_mtrics(loss=loss)
```

 * log artifacts
 
```python
tracking.log_artifact_ref(asset_path)
```

You can also use the callback instance to log extra information:

```python
from polyaxon.tracking.contrib.pytorch_lightning import PolyaxonCallback

callback = PolyaxonCallback()
callback.experiment.log_...
```

## Example

In this example we will go through the process of logging a Pytorch-Lightning model using Polyaxon's callback.

This example can be used with the offline mode `POLYAXON_OFFLINE=true` and it does not require a Polyaxon API to run locally. 

```python
import os

import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision import transforms
import pytorch_lightning as pl

from polyaxon.tracking.contrib.pytorch_lightning import PolyaxonCallback


class MNISTModel(pl.LightningModule):

    def __init__(self):
        super(MNISTModel, self).__init__()
        self.l1 = torch.nn.Linear(28 * 28, 10)

    def forward(self, x):
        return torch.relu(self.l1(x.view(x.size(0), -1)))

    def training_step(self, batch, batch_nb):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        tensorboard_logs = {'train_loss': loss}
        return {'loss': loss, 'log': tensorboard_logs}

    def validation_step(self, batch, batch_nb):
        x, y = batch
        y_hat = self(x)
        return {'val_loss': F.cross_entropy(y_hat, y)}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        tensorboard_logs = {'val_loss': avg_loss}
        return {'val_loss': avg_loss, 'log': tensorboard_logs}

    def test_step(self, batch, batch_nb):
        x, y = batch
        y_hat = self(x)
        return {'test_loss': F.cross_entropy(y_hat, y)}

    def test_epoch_end(self, outputs):
        avg_loss = torch.stack([x['test_loss'] for x in outputs]).mean()
        logs = {'test_loss': avg_loss}
        return {'test_loss': avg_loss, 'log': logs, 'progress_bar': logs}

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.02)

    def train_dataloader(self):
        return DataLoader(MNIST(os.getcwd(), train=True, download=True, transform=transforms.ToTensor()), batch_size=32)

    def val_dataloader(self):
        return DataLoader(MNIST(os.getcwd(), train=True, download=True, transform=transforms.ToTensor()), batch_size=32)

    def test_dataloader(self):
        return DataLoader(MNIST(os.getcwd(), train=False, download=True, transform=transforms.ToTensor()), batch_size=32)


train_loader = DataLoader(MNIST(os.getcwd(), train=True, download=True, transform=transforms.ToTensor()), batch_size=32)

mnist_model = MNISTModel()
trainer = pl.Trainer(
    gpus=0,
    progress_bar_refresh_rate=20,
    max_epochs=2,
    logger=PolyaxonCallback(),
)
trainer.fit(mnist_model, train_loader)
```

