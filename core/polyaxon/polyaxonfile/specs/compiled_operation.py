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
import copy

from typing import Dict, List

from polyaxon import types
from polyaxon.exceptions import PolyaxonfileError, PolyaxonSchemaError
from polyaxon.polyaxonfile.specs import BaseSpecification, kinds
from polyaxon.polyaxonfile.specs.libs.parser import Parser
from polyaxon.polyflow import ParamSpec, V1CompiledOperation, V1Dag, V1Init, V1Param


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
    def dict_to_param_spec(contexts: Dict = None, is_context: bool = False):
        contexts = contexts or {}
        return {
            k: ParamSpec(
                name=k,
                param=V1Param(value=v),
                iotype=types.ANY,
                is_flag=False,
                is_list=None,
                is_context=is_context,
                arg_format=None,
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
        param_spec = config.validate_params(
            is_template=False, check_runs=True, parse_values=True
        )
        if should_be_resolved:
            for p_spec in param_spec:
                if not p_spec.param.is_literal:
                    raise PolyaxonfileError(
                        "calculate_context_spec received a non-resolved "
                        "ref param `{}` with value `{}`".format(
                            p_spec.name, p_spec.param.to_dict()
                        )
                    )
        param_spec = {param.name: param for param in param_spec}
        param_spec.update(cls.dict_to_param_spec(contexts=contexts, is_context=True))
        return param_spec

    @classmethod
    def _apply_operation_contexts(
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
    def apply_operation_contexts(
        cls,
        config: V1CompiledOperation,
        param_spec: Dict[str, ParamSpec] = None,
        contexts: Dict = None,
    ) -> V1CompiledOperation:
        if config.is_dag_run:
            return cls._apply_dag_context(config)
        else:
            return cls._apply_operation_contexts(
                config=config, param_spec=param_spec, contexts=contexts
            )

    @classmethod
    def _apply_connections_params(
        cls,
        connections: List[str],
        init: List[V1Init],
        artifact_store: str = None,
        param_spec: Dict[str, ParamSpec] = None,
    ):
        if connections:
            connections = Parser.parse_section(
                connections, param_spec=param_spec, parse_params=True
            )
        _init = []
        if init:
            for i in init:
                if i.artifacts and not i.connection:
                    i.connection = artifact_store
                resolved_i = V1Init.from_dict(
                    Parser.parse_section(
                        i.to_dict(), param_spec=param_spec, parse_params=True
                    )
                )
                _init.append(resolved_i)

        # Prepend any param that has to_init after validation
        init_params = [v.to_init() for v in param_spec.values() if v.validate_to_init()]
        init_params = [v for v in init_params if v]
        _init = init_params + _init
        return _init, connections

    @classmethod
    def _apply_distributed_run_connections_params(
        cls,
        config: V1CompiledOperation,
        artifact_store: str = None,
        param_spec: Dict[str, ParamSpec] = None,
    ):
        def _resolve_replica(replica):
            if not replica:
                return
            init, connections = cls._apply_connections_params(
                init=replica.init,
                connections=replica.connections,
                artifact_store=artifact_store,
                param_spec=param_spec,
            )
            replica.init = init
            replica.connections = connections
            return replica

        if config.is_mpi_job_run:
            config.run.launcher = _resolve_replica(config.run.launcher)
            config.run.worker = _resolve_replica(config.run.worker)
        if config.is_tf_job_run:
            config.run.chief = _resolve_replica(config.run.chief)
            config.run.worker = _resolve_replica(config.run.worker)
            config.run.ps = _resolve_replica(config.run.ps)
            config.run.evaluator = _resolve_replica(config.run.evaluator)
        if config.is_pytorch_job_run:
            config.run.master = _resolve_replica(config.run.master)
            config.run.worker = _resolve_replica(config.run.worker)
        return config

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
        if config.is_job_run or config.is_service_run:
            init, connections = cls._apply_connections_params(
                init=config.run.init,
                connections=config.run.connections,
                artifact_store=artifact_store,
                param_spec=param_spec,
            )
            config.run.init = init
            config.run.connections = connections
            return config
        if config.is_distributed_run:
            return cls._apply_distributed_run_connections_params(
                config=config,
                artifact_store=artifact_store,
                param_spec=param_spec,
            )
        return config

    @classmethod
    def apply_params(
        cls,
        config: V1CompiledOperation,
        params: Dict = None,
        context: Dict = None,
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
    def _apply_runtime_contexts(
        cls,
        config: V1CompiledOperation,
        contexts: Dict = None,
        param_spec: Dict[str, ParamSpec] = None,
    ) -> V1CompiledOperation:
        if not param_spec:
            param_spec = cls.calculate_context_spec(
                config=config, contexts=contexts, should_be_resolved=True
            )
        parsed_data = Parser.parse_runtime(config.to_dict(), param_spec)
        return cls.CONFIG.read(parsed_data)

    @classmethod
    def _apply_distributed_runtime_contexts(
        cls,
        config: V1CompiledOperation,
        contexts: Dict = None,
        param_spec: Dict[str, ParamSpec] = None,
    ) -> V1CompiledOperation:
        if not param_spec:
            # Calculate the param_space once with empty contexts
            replica_param_spec = cls.calculate_context_spec(
                config=config, contexts=None, should_be_resolved=True
            )
            param_spec = {}
            for k in contexts:
                param_spec[k] = copy.copy(replica_param_spec)
                param_spec[k].update(
                    cls.dict_to_param_spec(contexts=contexts[k], is_context=True)
                )
        parsed_data = Parser.parse_distributed_runtime(config.to_dict(), param_spec)
        return cls.CONFIG.read(parsed_data)

    @classmethod
    def apply_runtime_contexts(
        cls,
        config: V1CompiledOperation,
        contexts: Dict = None,
        param_spec: Dict[str, ParamSpec] = None,
    ) -> V1CompiledOperation:
        if config.has_pipeline:
            raise PolyaxonSchemaError(
                "This method is not allowed on this specification."
            )
        if config.is_distributed_run:
            return cls._apply_distributed_runtime_contexts(
                config=config,
                contexts=contexts,
                param_spec=param_spec,
            )
        else:
            return cls._apply_runtime_contexts(
                config=config,
                contexts=contexts,
                param_spec=param_spec,
            )
