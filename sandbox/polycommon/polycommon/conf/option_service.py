#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from typing import Any, Optional

from polyaxon.exceptions import PolyaxonException
from polycommon.conf.conf_manager import conf_cache_manager
from polycommon.conf.exceptions import ConfException
from polycommon.conf.option_manager import option_manager
from polycommon.options.option import Option
from polycommon.options.option_owners import OptionOwners
from polycommon.service_interface import Service


class OptionService(Service):
    __all__ = ("get", "set", "delete", "clear_cache", "get_owners")

    option_manager = option_manager
    cache_manager = conf_cache_manager
    service_name = "Option"

    def __init__(self, check_ownership=False):
        self.stores = {}
        self.check_ownership = check_ownership

    def get_options_handler(self):
        return None

    def can_handle(self, key: str) -> bool:
        return isinstance(key, str) and self.option_manager.knows(key=key)

    def get_option(self, key: str, owners: OptionOwners) -> Option:
        option = self.option_manager.get(key=key)
        if self.check_ownership and not option.is_global():
            if not owners or not [i for i in owners if i]:
                raise ConfException("Option `{}` requires an owner.".format(option.key))
        return option

    def get_store(self, option: Option) -> Any:
        if option.store not in self.stores:
            raise ConfException("Option `{}` has an invalid store.".format(option.key))

        return self.stores[option.store]

    @staticmethod
    def _get_value(option, value, to_dict):
        if not to_dict:
            return value
        option_dict = option.to_dict(value=value)
        return option_dict

    def get(
        self,
        key: str,
        check_cache: bool = True,
        to_dict: bool = False,
        owners: Optional[OptionOwners] = None,
    ) -> Any:
        if not self.is_setup:
            return
        if not self.can_handle(key=key):
            raise ConfException(
                "{} service request an unknown key `{}`.".format(self.service_name, key)
            )

        option = self.get_option(key=key, owners=owners)

        if check_cache:
            value = self.cache_manager.get_from_cache(key=key, owners=owners)
            if self.cache_manager.is_valid_value(value=value):
                return self._get_value(option=option, value=value, to_dict=to_dict)

        store = self.get_store(option=option)
        value = store.get(option=option, owners=owners)

        # Cache value
        self.cache_manager.set_to_cache(
            key=key, value=value, ttl=option.cache_ttl, owners=owners
        )

        return self._get_value(option=option, value=value, to_dict=to_dict)

    def set(self, key: str, value: Any, owners: Optional[OptionOwners] = None) -> None:
        if not self.is_setup:
            return
        if not self.can_handle(key=key):
            raise ConfException(
                "{} service request an unknown key `{}`.".format(self.service_name, key)
            )
        if value is None:
            raise ConfException(
                "{} service requires a value for key `{}` to set.".format(
                    self.service_name, key
                )
            )
        option = self.get_option(key=key, owners=owners)
        # Convert value
        try:
            value = option.parse(value=value)
        except PolyaxonException as e:
            raise ConfException(e)

        store = self.get_store(option=option)
        store.set(option=option, value=value, owners=owners)
        # Cache value
        self.cache_manager.set_to_cache(
            key=key, value=value, ttl=option.cache_ttl, owners=owners
        )

    def delete(self, key: str, owners: Optional[OptionOwners] = None) -> None:
        if not self.is_setup:
            return
        if not self.can_handle(key=key):
            raise ConfException(
                "{} service request an unknown key `{}`.".format(self.service_name, key)
            )

        option = self.get_option(key=key, owners=owners)
        store = self.get_store(option=option)
        store.delete(option=option, owners=owners)
        # Clear Cache key
        self.cache_manager.clear_key(key=key, owners=owners)

    def clear_cache(self) -> None:
        self.cache_manager.clear()

    @staticmethod
    def get_owners(
        user: int = None, project: int = None, organization: int = None
    ) -> OptionOwners:
        return OptionOwners.get_owners(
            user=user, project=project, organization=organization
        )
