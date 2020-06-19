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
    def dict_to_param_spec(contexts: Dict = None):
        contexts = contexts or {}
        return {
            k: ParamSpec(
                name=k,
                param=V1Param(value=v),
                iotype=types.ANY,
                is_flag=False,
                is_list=None,
            )
            for k, v in contexts.items()
        }

    @classmethod
    def calculate_context_spec(
        cls,
        config: V1CompiledOperation,
        contexts: Dict = None,
        should_be_resolved: bool = False,
    ) -> Dict[str, ParamSpec]:
        param_spec = config.validate_params(is_template=False, check_runs=True)
        if should_be_resolved:
            for p_spec in param_spec:
                if not p_spec.param.is_literal:
                    raise PolyaxonfileError(
                        "apply_run_context received a non-resolved "
                        "ref param `{}` with value `{}`".format(
                            p_spec.name, p_spec.param.to_dict()
                        )
                    )
        param_spec = {param.name: param for param in param_spec}
        param_spec.update(cls.dict_to_param_spec(contexts=contexts))
        return param_spec

    @classmethod
    def _apply_run_context(
        cls,
        config: V1CompiledOperation,
        param_spec: Dict[str, ParamSpec] = None,
        contexts: Dict = None,
    ) -> V1CompiledOperation:
        if not param_spec:
            param_spec = cls.calculate_context_spec(config=config, contexts=contexts)
        return cls._parse(config, param_spec)

    @staticmethod
    def _apply_dag_context(config: V1CompiledOperation) -> V1CompiledOperation:
        dag_run = config.run  # type: V1Dag
        dag_run.process_dag()
        dag_run.validate_dag()
        dag_run.process_components(config.inputs)
        return config

    @classmethod
    def apply_run_context(
        cls,
        config: V1CompiledOperation,
        param_spec: Dict[str, ParamSpec] = None,
        contexts: Dict = None,
    ) -> V1CompiledOperation:
        if config.is_dag_run:
            return cls._apply_dag_context(config)
        else:
            return cls._apply_run_context(
                config=config, param_spec=param_spec, contexts=contexts
            )

    @classmethod
    def apply_run_connections_params(
        cls,
        config: V1CompiledOperation,
        artifact_store: str = None,
        contexts: Dict = None,
        param_spec: Dict[str, ParamSpec] = None,
    ) -> V1CompiledOperation:
        if not param_spec:
            param_spec = cls.calculate_context_spec(config=config, contexts=contexts)
        if config.run.kind in {V1RunKind.JOB, V1RunKind.SERVICE}:
            if config.run.connections:
                config.run.connections = Parser.parse_section(
                    config.run.connections, param_spec=param_spec, parse_params=True
                )
            if config.run.init:
                init = []
                for i in config.run.init:
                    if i.artifacts and not i.connection:
                        i.connection = artifact_store
                    resolved_i = V1Init.from_dict(
                        Parser.parse_section(
                            i.to_dict(), param_spec=param_spec, parse_params=True
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
    def apply_section_contexts(
        cls,
        config: V1CompiledOperation,
        section,
        contexts: Dict = None,
        param_spec: Dict[str, ParamSpec] = None,
    ):
        if not param_spec:
            param_spec = cls.calculate_context_spec(config=config, contexts=contexts)

        return Parser.parse_section(section, param_spec)

    @classmethod
    def apply_operation_contexts(
        cls,
        config: V1CompiledOperation,
        contexts: Dict = None,
        param_spec: Dict[str, ParamSpec] = None,
    ):
        if config.has_pipeline:
            raise PolyaxonSchemaError(
                "This method is not allowed on this specification."
            )
        if not param_spec:
            param_spec = cls.calculate_context_spec(config=config, contexts=contexts)

        parsed_data = Parser.parse_run(config.to_dict(), param_spec)
        return cls.CONFIG.read(parsed_data)
