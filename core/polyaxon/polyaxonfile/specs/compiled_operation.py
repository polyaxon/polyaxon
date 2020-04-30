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
from typing import Dict

from polyaxon import types
from polyaxon.exceptions import PolyaxonfileError, PolyaxonSchemaError
from polyaxon.polyaxonfile.specs import BaseSpecification, kinds
from polyaxon.polyaxonfile.specs.libs.parser import Parser
from polyaxon.polyflow import (  # noqa
    ParamSpec,
    V1CompiledOperation,
    V1Dag,
    V1Init,
    V1Param,
    V1RunKind,
)


class CompiledOperationSpecification(BaseSpecification):
    """The polyaxonfile specification for compiled operation."""

    _SPEC_KIND = kinds.COMPILED_OPERATION

    CONFIG = V1CompiledOperation

    @classmethod
    def _parse(cls, config, params: Dict[str, ParamSpec]):
        params = params or {}
        parsed_data = Parser.parse(config, params)
        return cls.CONFIG.read(parsed_data)

    @staticmethod
    def _update_params_with_contexts(
        params: Dict[str, ParamSpec], contexts: Dict = None
    ) -> Dict[str, ParamSpec]:
        contexts = contexts or {}
        contexts = {
            k: ParamSpec(
                name=k,
                param=V1Param(value=v),
                iotype=types.ANY,
                is_flag=False,
                is_list=None,
            )
            for k, v in contexts.items()
        }
        params.update(contexts)
        return params

    @classmethod
    def _apply_run_context(cls, config: V1CompiledOperation) -> V1CompiledOperation:
        param_specs = config.validate_params(is_template=False, check_runs=True)

        for param_spec in param_specs:
            if not param_spec.param.is_literal:
                raise PolyaxonfileError(
                    "apply_context received a non-resolved "
                    "ref param `{}` with value `{}`".format(
                        param_spec.name, param_spec.param.to_dict()
                    )
                )

        param_specs = {param_spec.name: param_spec for param_spec in param_specs}
        return cls._parse(config, param_specs)

    @staticmethod
    def _apply_dag_context(config: V1CompiledOperation) -> V1CompiledOperation:
        dag_run = config.run  # type: V1Dag
        dag_run.process_dag()
        dag_run.validate_dag()
        dag_run.process_components(config.inputs)
        return config

    @classmethod
    def apply_context(cls, config: V1CompiledOperation) -> V1CompiledOperation:
        if config.is_dag_run:
            return cls._apply_dag_context(config)
        else:
            return cls._apply_run_context(config)

    @classmethod
    def apply_run_connections_params(
        cls,
        config: V1CompiledOperation,
        artifact_store: str = None,
        contexts: Dict = None,
    ) -> V1CompiledOperation:
        params = config.validate_params(is_template=False, check_runs=True)
        params = {param.name: param for param in params}
        params = cls._update_params_with_contexts(params, contexts)
        if config.run.kind in {V1RunKind.JOB, V1RunKind.SERVICE}:
            if config.run.connections:
                config.run.connections = Parser.parse_section(
                    config.run.connections, params=params, parse_params=True
                )
            if config.run.init:
                init = []
                for i in config.run.init:
                    if i.artifacts and not i.connection:
                        i.connection = artifact_store
                    resolved_i = V1Init.from_dict(
                        Parser.parse_section(
                            i.to_dict(), params=params, parse_params=True
                        )
                    )
                    init.append(resolved_i)
                config.run.init = init
        return config

    @classmethod
    def apply_params(
        cls, config: V1CompiledOperation, params: Dict = None, context: Dict = None,
    ) -> V1CompiledOperation:
        config.apply_params(params, context)
        return config

    @classmethod
    def apply_run_contexts(cls, config: V1CompiledOperation, contexts=None):
        if config.has_pipeline:
            raise PolyaxonSchemaError(
                "This method is not allowed on this specification."
            )
        params = config.validate_params(is_template=False, check_runs=True)
        params = {param.name: param for param in params}
        params = cls._update_params_with_contexts(params, contexts)
        parsed_data = Parser.parse_run(config.to_dict(), params)
        return cls.CONFIG.read(parsed_data)
