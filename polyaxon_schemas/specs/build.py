# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from hestia.cached_property import cached_property
from marshmallow import EXCLUDE

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.ops.build import BuildConfig
from polyaxon_schemas.specs.base import BaseSpecification, EnvironmentSpecificationMixin


class BuildSpecification(BaseSpecification, EnvironmentSpecificationMixin):
    """The polyaxonfile specification for build jobs.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = BaseSpecification._BUILD

    BUILD_STEPS = 'build_steps'
    ENV_VARS = 'env_vars'
    NOCACHE = 'nocache'
    BRANCH = 'branch'
    COMMIT = 'commit'
    CONTEXT = 'context'
    DOCKERFILE = 'dockerfile'
    IMAGE = 'image'

    SECTIONS = BaseSpecification.SECTIONS + (
        BUILD_STEPS, ENV_VARS, NOCACHE, BRANCH, COMMIT, CONTEXT, DOCKERFILE, IMAGE)

    OP_PARSING_SECTIONS = BaseSpecification.OP_PARSING_SECTIONS + (
        BUILD_STEPS, ENV_VARS, NOCACHE, BRANCH, COMMIT, CONTEXT, DOCKERFILE, IMAGE)

    HEADER_SECTIONS = BaseSpecification.HEADER_SECTIONS + (BaseSpecification.BACKEND, )

    POSSIBLE_SECTIONS = BaseSpecification.POSSIBLE_SECTIONS + (
        BaseSpecification.BACKEND, BaseSpecification.ENVIRONMENT,
        BUILD_STEPS, ENV_VARS, NOCACHE, BRANCH, COMMIT, CONTEXT, DOCKERFILE, IMAGE
    )

    CONFIG = BuildConfig

    @cached_property
    def backend(self):
        return self.config.backend

    @classmethod
    def create_specification(cls,
                             build_config,
                             secret_refs=None,
                             configmap_refs=None,
                             to_dict=True):
        if isinstance(build_config, BuildConfig):
            config = build_config.to_light_dict()
        elif isinstance(build_config, Mapping):
            # Since the objective is to create the build spec from other specs
            # we drop any extra attrs
            config = BuildConfig.from_dict(build_config, unknown=EXCLUDE)
            config = config.to_light_dict()
        else:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of BuildConfig.')

        specification = {
            cls.VERSION: 1,
            cls.KIND: cls._SPEC_KIND,
        }
        specification.update(config)

        env = {}
        if secret_refs:
            env['secret_refs'] = secret_refs
        if configmap_refs:
            env['configmap_refs'] = configmap_refs
        if env:
            specification[cls.ENVIRONMENT] = env

        if to_dict:
            return specification
        return cls.read(specification)
