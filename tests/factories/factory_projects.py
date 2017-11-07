# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import factory

from projects.models import Project, Polyaxonfile

from tests.factories.factory_users import UserFactory


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda x: "project-{}".format(x))

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Project


class PolyaxonfileFactory(factory.DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Polyaxonfile
