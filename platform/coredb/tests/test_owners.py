#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from django.db import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from coredb.factories.projects import ProjectFactory
from coredb.factories.users import UserFactory
from coredb.managers.owners import (
    create_owner,
    delete_owner,
    has_owner,
    validate_owner_name,
)
from coredb.models.owners import Owner


class TestOwnerModel(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.owner = Owner.objects.filter(name=self.user.username).last()

    def test_has_owner(self):
        project = ProjectFactory(owner_id=self.owner.id)
        assert has_owner(project) is True

    def test_create_owner_already_exists_raises(self):
        with self.assertRaises(IntegrityError):
            create_owner(name=self.user.username, uuid=uuid.uuid4())

    def test_create_owner(self):
        assert Owner.objects.count() == 1
        user = UserFactory()
        with self.assertRaises(IntegrityError):
            create_owner(user.username, uuid=uuid.uuid4())

    def test_delete_owner(self):
        assert Owner.objects.count() == 1
        delete_owner("foo")  # Does not do anything
        assert Owner.objects.count() == 1

        delete_owner(self.owner.name)
        assert Owner.objects.count() == 0

    def test_validate_owner_name(self):
        with self.assertRaises(ValidationError):
            validate_owner_name(self.user.username)

        # Other username does not raise
        validate_owner_name("foo")
