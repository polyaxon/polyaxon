# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from collections import namedtuple

from marshmallow import fields, validate

from polyaxon_schemas.base import NAME_REGEX
from polyaxon_schemas.exceptions import PolyaxonSchemaError
from polyaxon_schemas.ops import params as ops_params
from polyaxon_schemas.ops.logging import LoggingSchema
from polyaxon_schemas.polyflow.executable import ExecutableConfig, ExecutableSchema
from polyaxon_schemas.polyflow.ops import OpSchema
from polyaxon_schemas.polyflow.schedule import ScheduleSchema
from polyaxon_schemas.polyflow.template import TemplateSchema


class DagOpSpec(namedtuple("DagOpSpec", "op upstream downstream")):

    def items(self):
        return self._asdict().items()

    def set_op(self, op):
        return self._replace(op=op)


class PipelineSchema(ExecutableSchema):
    version = fields.Int(allow_none=True)
    kind = fields.Str(allow_none=True, validate=validate.Equal('pipeline'))
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    description = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    logging = fields.Nested(LoggingSchema, allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    backend = fields.Str(allow_none=True)
    ops = fields.Nested(OpSchema, many=True)
    templates = fields.Nested(TemplateSchema, many=True)
    schedule = fields.Nested(ScheduleSchema, allow_none=True)
    concurrency = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return PipelineConfig


class PipelineConfig(ExecutableConfig):
    SCHEMA = PipelineSchema
    IDENTIFIER = 'pipeline'
    REDUCED_ATTRIBUTES = ExecutableConfig.REDUCED_ATTRIBUTES + [
        'kind',
        'version',
        'name',
        'description',
        'logging',
        'tags',
        'backend',
        'ops',
        'concurrency',
        'schedule',
        'templates',
    ]

    def __init__(self,
                 kind=None,
                 version=None,
                 name=None,
                 description=None,
                 logging=None,
                 tags=None,
                 backend=None,
                 ops=None,
                 concurrency=None,
                 schedule=None,
                 templates=None,
                 execute_at=None,
                 timeout=None):
        super(PipelineConfig, self).__init__(execute_at=execute_at, timeout=timeout)
        self.kind = kind
        self.version = version
        self.name = name
        self.description = description
        self.logging = logging
        self.tags = tags
        self.backend = backend
        self.ops = ops
        self.concurrency = concurrency
        self.schedule = schedule
        self.templates = templates
        self._dag = {}  # OpName -> DagOpSpec
        self._template_by_names = {}  # TemplateName -> Template
        self._op_template_mapping = {}  # OpName -> TemplateName
        self._context = {}  # Ops output names -> IOTypes

    @property
    def dag(self):
        return self._dag

    def validate_dag(self, dag=None):
        dag = dag or self.dag
        orphan_ops = self.get_orphan_ops(dag=dag)
        if orphan_ops:
            raise PolyaxonSchemaError('Pipeline has a non valid dag, the dag contains orphan ops: '
                                      '`{}`'.format(orphan_ops))
        self.sort_topologically(dag=dag)

    def _get_op_upstream(self, op):
        upstream = set(op.dependencies) if op.dependencies else set([])

        if not op.params:
            return upstream

        for param in op.params:
            param_ref = ops_params.get_param(name=param,
                                             value=op.params[param],
                                             iotype=None,
                                             is_flag=None)
            if param_ref and param_ref.entity == ops_params.OPS:
                upstream.add(param_ref.entity_ref)

        return upstream

    def _set_dag_op(self, op_name, op=None, upstream=None, downstream=None):
        upstream = set(upstream) if upstream else set([])
        downstream = set(downstream) if downstream else set([])
        if op_name in self._dag:
            if op and self._dag[op_name].op is None:
                self._dag[op_name] = self._dag[op_name].set_op(op)
            self._dag[op_name].upstream.update(upstream)
            self._dag[op_name].downstream.update(downstream)
        else:
            self._dag[op_name] = DagOpSpec(op=op, upstream=upstream, downstream=downstream)

    def _process_op(self, op):
        upstream = self._get_op_upstream(op=op)
        self._set_dag_op(op_name=op.name, op=op, upstream=upstream, downstream=None)
        for op_name in upstream:
            self._set_dag_op(op_name=op_name, downstream=[op.name])

    def process_dag(self):
        for op in self.ops or []:
            self._process_op(op)

    def add_op(self, op):
        self.ops = self.ops or []
        self.ops.append(op)
        self._process_op(op)

    def add_ops(self, ops):
        for op in ops:
            self.add_op(op)

    def get_independent_ops(self, dag=None):
        """Get a list of all node in the graph with no dependencies."""
        dag = dag or self.dag
        ops = set(six.iterkeys(dag))
        dependent_nodes = {op_downstream for op in six.itervalues(dag)
                           for op_downstream in op.downstream}
        return ops - dependent_nodes

    def get_orphan_ops(self, dag=None):
        """Get orphan ops for given dag."""
        dag = dag or self.dag
        independent_ops = self.get_independent_ops(dag)
        return {op for op in independent_ops if dag[op].op is None}

    def sort_topologically(self, dag=None, flatten=False):
        """Sort the dag breath first topologically.

        Only the nodes inside the dag are returned, i.e. the nodes that are also keys.

        Returns:
             a topological ordering of the DAG.
        Raises:
             an error if this is not possible (graph is not valid).
        """
        def get_independent_ops():
            if current_independent_ops:
                return current_independent_ops.pop()
            current_independent_ops.update(next_independent_ops)
            next_independent_ops.clear()
            sorted_ops.append(current_sorted_ops[:])
            del current_sorted_ops[:]  # in python3 it should use .clear()
            if current_independent_ops:
                return current_independent_ops.pop()

        dag = dag or self.dag
        visited_ops = set()
        next_independent_ops = set()
        current_sorted_ops = []
        sorted_ops = []
        current_independent_ops = self.get_independent_ops(dag)
        op = get_independent_ops()
        while op:
            current_sorted_ops.append(op)
            visited_ops.add(op)
            downstream_ops = dag[op].downstream.copy()
            while downstream_ops:
                downstream_op = downstream_ops.pop()

                if downstream_op not in dag:
                    continue

                if downstream_op in visited_ops:
                    continue

                if not dag[downstream_op].upstream - visited_ops:
                    next_independent_ops.add(downstream_op)

            op = get_independent_ops()

        flatten_sorted_ops = [i for il in sorted_ops for i in il]
        if len(flatten_sorted_ops) != len(dag.keys()):
            raise PolyaxonSchemaError("Pipeline's graph is not acyclic.")
        return flatten_sorted_ops if flatten else sorted_ops

    def process_templates(self):
        if not self.templates:
            raise PolyaxonSchemaError('Pipeline is not valid, '
                                      'it has no templates to validate operations.')

        if not self.ops:
            raise PolyaxonSchemaError('Pipeline is not valid, '
                                      'it has no ops to validate operations.')

        for template in self.templates:
            template_name = template.name
            if template_name in self._template_by_names:
                raise PolyaxonSchemaError(
                    'Pipeline has multiple templates with the same name `{}`'.format(template_name))
            self._template_by_names[template_name] = template

        for op in self.ops:
            op_name = op.name
            template_name = op.template.name
            if op_name in self._op_template_mapping:
                raise PolyaxonSchemaError(
                    'Pipeline has multiple ops with the same name `{}`'.format(op_name))

            if template_name not in self._template_by_names:
                raise PolyaxonSchemaError(
                    'Pipeline op with name `{}` requires a template with name `{}`, '
                    'which is not defined on this pipeline.'.format(op_name, template_name))

            self._op_template_mapping[op_name] = template_name
            outputs = self._template_by_names[template_name].outputs
            if not outputs:
                continue
            for output in outputs:
                self._context['ops.{}.outputs.{}'.format(op_name, output.name)] = output

        for op in self.ops:
            template = self._template_by_names[self._op_template_mapping[op.name]]
            ops_params.validate_params(params=op.params,
                                       inputs=template.inputs,
                                       outputs=template.outputs,
                                       context=self._context,
                                       is_template=False,
                                       is_run=False)
