# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import factory

from projects.models import Project, PolyaxonSpec

from tests.factories.factory_users import UserFactory


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: "project-{}".format(x))

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Project


class PolyaxonSpecFactory(factory.DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)
    content = """---
version: 1

project:
  name: project1

model:
  model_type: regressor
  loss:
    MeanSquaredError:
  optimizer:
    Adam:
  graph:
    input_layers: images
    layers:
      - Conv2D:
          filters: 64
          kernel_size: [3, 3]
          strides: [1, 1]
          activation: relu
          kernel_initializer: Ones
      - MaxPooling2D:
          kernels: 2
      - Flatten:
      - Dense:
          units: 10
          activation: softmax
        
train:
  data_pipeline:
    TFRecordImagePipeline:
      batch_size: 64
      num_epochs: 1
      shuffle: true
      dynamic_pad: false
      data_files: ["../data/mnist/mnist_train.tfrecord"]
      meta_data_file: "../data/mnist/meta_data.json"

    """

    class Meta:
        model = PolyaxonSpec
