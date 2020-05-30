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

import inspect
import itertools

from polyaxon.utils.imports import import_string

try:
    from django.utils.functional import LazyObject, empty  # pylint:disable=import-error
except ImportError:
    raise ImportError("This module depends on django.")


class InvalidService(Exception):
    pass


class Service:
    __all__ = ()
    is_setup = False

    def validate(self):
        """Validate the settings for this backend (i.e. such as proper connection info).

        Raise ``InvalidService`` if there is a configuration error.
        """

    def setup(self):
        """Initialize this service."""
        self.is_setup = True

    def validate_and_setup(self):
        self.validate()
        self.setup()


class LazyServiceWrapper(LazyObject):
    """Lazyily instantiates a Polyaxon standard service class.

    >>> LazyServiceWrapper(BaseClass, 'path.to.import.Backend', {})

    Provides an ``expose`` method for dumping public APIs to a context, such as module locals:

    >>> service = LazyServiceWrapper(...)
    >>> service.expose(locals())
    """

    def __init__(self, backend_base, backend_path, options):
        super().__init__()
        self.__dict__.update(
            {
                "_backend_base": backend_base,
                "_backend_path": backend_path,
                "_options": options,
            }
        )

    def __getattr__(self, name):
        if self._wrapped is empty:  # pylint:disable=attribute-defined-outside-init
            self._setup()
        return getattr(self._wrapped, name)

    def _setup(self):
        backend = import_string(self._backend_path)
        assert issubclass(backend, Service)
        instance = backend(**self._options)
        self._wrapped = instance  # pylint:disable=attribute-defined-outside-init

    def expose(self, context):
        base = self._backend_base
        for key in itertools.chain(
            base.__all__, ("validate", "setup", "validate_and_setup")
        ):
            if inspect.isfunction(getattr(base, key)):
                # pylint:disable=unnecessary-lambda
                # pylint:disable=undefined-variable
                context[key] = (lambda f: lambda *a, **k: getattr(self, f)(*a, **k))(
                    key
                )
            else:
                context[key] = getattr(base, key)
