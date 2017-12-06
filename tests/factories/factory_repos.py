# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import factory
from faker import Factory as FakerFactory

from repos.models import Repo
from tests.factories.factory_projects import ProjectFactory
from tests.factories.factory_users import UserFactory

fake = FakerFactory.create()


class RepoFactory(factory.DjangoModelFactory):
    class Meta:
        model = Repo

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
