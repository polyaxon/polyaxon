# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import factory
from faker import Factory as FakerFactory

from factories.factory_users import UserFactory
from factories.fixtures import tensorboard_spec_parsed_content
from plugins.models import TensorboardJob

fake = FakerFactory.create()


class TensorboardJobFactory(factory.DjangoModelFactory):
    config = tensorboard_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = TensorboardJob
