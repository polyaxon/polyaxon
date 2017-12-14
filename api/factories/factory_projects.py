# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import factory

from factories.fixtures import experiment_group_spec_content_2_xps
from projects.models import Project, ExperimentGroup

from factories.factory_users import UserFactory


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: "project-{}".format(x))

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Project


class ExperimentGroupFactory(factory.DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda x: "group-{}".format(x))
    content = experiment_group_spec_content_2_xps

    class Meta:
        model = ExperimentGroup
