# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from factories.fixtures import tensorboard_spec_parsed_content
from plugins.models import TensorboardJob
from plugins.serializers import (
    TensorboardJobSerializer,
)
from factories.factory_plugins import TensorboardJobFactory

from tests.utils import BaseTest


class TestTensorboardJobSerializer(BaseTest):
    serializer_class = TensorboardJobSerializer
    model_class = TensorboardJob
    factory_class = TensorboardJobFactory

    def test_validation_raises_for_invalid_data(self):
        # No data
        serializer = self.serializer_class(data={})
        assert serializer.is_valid() is False

        # Wrong spec
        serializer = self.serializer_class(data={'config': {}})
        assert serializer.is_valid() is False

    def test_validation_passes_for_valid_data(self):
        serializer = self.serializer_class(
            data={'config': tensorboard_spec_parsed_content.parsed_data})
        assert serializer.is_valid() is True

    def creating_tensorboard_job_from_valid_data(self):
        assert TensorboardJob.objects.count() == 0
        serializer = self.serializer_class(
            data={'config': tensorboard_spec_parsed_content.parsed_data})
        serializer.is_valid()
        serializer.save()
        assert TensorboardJob.objects.count() == 1

    def updating_tensorboard_job(self):
        tb = TensorboardJobFactory()
        assert tb.config['version'] == 1
        config = tensorboard_spec_parsed_content.parsed_data
        config['version'] = 2
        serializer = self.serializer_class(
            instance=tb,
            data={'config': config})
        serializer.is_valid()
        serializer.save()
        tb.refresh_from_db()
        assert tb.config['version'] == 2
