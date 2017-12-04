# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import factory

from experiments.models import (
    Experiment,
    ExperimentStatus,
    ExperimentJob,
    ExperimentJobStatus,
)
from tests.factories.factory_clusters import ClusterFactory
from tests.factories.factory_projects import ProjectFactory

from tests.factories.factory_users import UserFactory


class ExperimentFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: "experiment-{}".format(x))
    config = {}  # TODO this should be a valid config

    user = factory.SubFactory(UserFactory)
    cluster = factory.SubFactory(ClusterFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Experiment


class ExperimentMetricFactory(factory.DjangoModelFactory):
    experiment = factory.SubFactory(ExperimentFactory)
    values = factory.Sequence(lambda x: {'accuracy': x})


class ExperimentStatusFactory(factory.DjangoModelFactory):
    experiment = factory.SubFactory(ExperimentFactory)

    class Meta:
        model = ExperimentStatus


class ExperimentJobFactory(factory.DjangoModelFactory):
    definition = {}  # TODO should be a valid k8s config
    experiment = factory.SubFactory(ExperimentFactory)

    class Meta:
        model = ExperimentJob


class ExperimentJobStatusFactory(factory.DjangoModelFactory):
    job = factory.SubFactory(ExperimentJobFactory)

    class Meta:
        model = ExperimentJobStatus
