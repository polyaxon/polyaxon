# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import factory

from experiments.models import (
    Experiment,
    ExperimentStatus,
    ExperimentJob,
    ExperimentJobStatus,
)
from factories.factory_projects import ProjectFactory

from factories.factory_users import UserFactory
from factories.fixtures import exec_experiment_spec_parsed_content


class ExperimentFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: "experiment-{}".format(x))
    config = exec_experiment_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)
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
