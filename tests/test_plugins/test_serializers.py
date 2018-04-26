from django.test import tag

from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.fixtures import plugin_spec_parsed_content
from plugins.models import NotebookJob, TensorboardJob
from plugins.serializers import NotebookJobSerializer, TensorboardJobSerializer
from tests.utils import RUNNER_TEST, BaseTest


@tag(RUNNER_TEST)
class BasePluginJobSerializerTest(BaseTest):
    model_class = None
    serializer_class = None
    factory_class = None

    def test_validation_raises_for_invalid_data(self):
        # No data
        serializer = self.serializer_class(data={})  # pylint:disable=not-callable
        assert serializer.is_valid() is False

        # Wrong spec
        serializer = self.serializer_class(data={'config': {}})  # pylint:disable=not-callable
        assert serializer.is_valid() is False

    def test_validation_passes_for_valid_data(self):
        serializer = self.serializer_class(  # pylint:disable=not-callable
            data={'config': plugin_spec_parsed_content.parsed_data})
        assert serializer.is_valid() is True

    def creating_plugin_job_from_valid_data(self):
        assert self.model_class.objects.count() == 0
        serializer = self.serializer_class(  # pylint:disable=not-callable
            data={'config': plugin_spec_parsed_content.parsed_data})
        serializer.is_valid()
        serializer.save()
        assert self.model_class.objects.count() == 1

    def updating_plugin_job(self):
        obj = self.factory_class()  # pylint:disable=not-callable
        assert obj.config['version'] == 1
        config = plugin_spec_parsed_content.parsed_data
        config['version'] = 2
        serializer = self.serializer_class(  # pylint:disable=not-callable
            instance=obj,
            data={'config': config})
        serializer.is_valid()
        serializer.save()
        obj.refresh_from_db()
        assert obj.config['version'] == 2


@tag(RUNNER_TEST)
class TestTensorboardJobSerializer(BaseTest):
    serializer_class = TensorboardJobSerializer
    model_class = TensorboardJob
    factory_class = TensorboardJobFactory


@tag(RUNNER_TEST)
class TestNotebookJobSerializer(BaseTest):
    serializer_class = NotebookJobSerializer
    model_class = NotebookJob
    factory_class = NotebookJobFactory


# Prevent this base class from running tests
del BasePluginJobSerializerTest
