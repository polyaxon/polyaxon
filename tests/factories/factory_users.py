# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import factory
from faker import Factory as FakerFactory

from django.conf import settings


fake = FakerFactory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.LazyAttribute(lambda x: fake.user_name())
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())
    email = factory.LazyAttribute(lambda x: fake.email())
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    is_staff = False
