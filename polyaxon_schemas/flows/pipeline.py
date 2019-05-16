# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.flows.executable import ExecutableConfig, ExecutableSchema
from polyaxon_schemas.flows.op import OpSchema
from polyaxon_schemas.flows.schedule import ScheduleSchema
from polyaxon_schemas.ops.logging import LoggingSchema


class PipelineSchema(ExecutableSchema):
    version = fields.Int(allow_none=None)
    kind = fields.Str(allow_none=None, validate=validate.Equal('pipeline'))
    name = fields.Str(allow_none=None)
    logging = fields.Nested(LoggingSchema, allow_none=None)
    tags = fields.List(fields.Str(), allow_none=None)
    backend = fields.Str(allow_none=True)
    ops = fields.Nested(OpSchema, many=True)
    schedule = fields.Nested(ScheduleSchema, allow_none=True)
    concurrency = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return PipelineConfig


class PipelineConfig(ExecutableConfig):
    SCHEMA = PipelineSchema
    IDENTIFIER = 'pipeline'
    REDUCED_ATTRIBUTES = [
        'kind',
        'version',
        'name',
        'logging',
        'tags',
        'backend',
        'operations'
    ]

    def __init__(self,
                 kind=None,
                 version=None,
                 name=None,
                 logging=None,
                 tags=None,
                 backend=None,
                 ops=None,
                 concurrency=None,
                 schedule=None,
                 execute_at=None,
                 timeout=None):
        super(PipelineConfig, self).__init__(execute_at=execute_at, timeout=timeout)
        self.kind = kind
        self.version = version
        self.name = name
        self.logging = logging
        self.tags = tags
        self.backend = backend
        self.ops = ops
        self.concurrency = concurrency
        self.schedule = schedule

    def add_operation(self, operation):
        self.ops.append(operation)

    def add_operations(self, operations):
        for op in operations:
            self.ops.append(op)

    @staticmethod
    def get_dag(nodes, downstream_fn, node_id_fn):
        """Return a dag representation of the nodes passed.

        This is equally used for pipelines and pipeline runs.

        Params:
            nodes: an instance of `BaseOpConfig` | `Operation` | `OperationRun`,
                   the nodes to represent the dag.
            downstream_fn: a function that returns the downstream nodes of the a node.
            op_id_fn: a function that returns a unique id of the node, e.g. op.id, op.uuid, op.name

        Returns:
             tuple: (dag, dict(node_id: node))
        """
        dag = {}
        node_by_ids = {}
        for node in nodes:
            downstream_ops = downstream_fn(node)
            node_id = node_id_fn(node)
            dag[node_id] = set(downstream_ops)
            node_by_ids[node_id] = node

        return dag, node_by_ids
