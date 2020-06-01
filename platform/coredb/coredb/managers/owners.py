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

from typing import Any
from uuid import UUID

from rest_framework.exceptions import ValidationError

from coredb.models.owners import Owner


def has_owner(obj: Any) -> bool:
    """Quick test to check the instance has an owner."""
    return bool(obj.owner_id)


def create_owner(name: str, uuid: UUID) -> Owner:
    return Owner.objects.create(name=name, uuid=uuid)


def delete_owner(name: str) -> None:
    try:
        Owner.objects.get(name=name).delete()
    except Owner.DoesNotExist:
        # Fail silently
        pass


def validate_owner_name(name: str) -> None:
    if Owner.objects.filter(name__iexact=name).exists():
        raise ValidationError("The name is a reserved word or already taken.")
