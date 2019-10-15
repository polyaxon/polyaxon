# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon.schemas.base import BaseOneOfSchema
from polyaxon.schemas.exceptions import PolyaxonSchemaError
from polyaxon.schemas.ops import params as ops_params
from polyaxon.schemas.ops.job import JobConfig, JobSchema
from polyaxon.schemas.ops.operation import BaseOpConfig, BaseOpSchema
from polyaxon.schemas.ops.service import ServiceConfig, ServiceSchema
from polyaxon.schemas.pkg import SCHEMA_VERSION
from polyaxon.schemas.polyflow import dags
from polyaxon.schemas.polyflow.ops import OpSchema
from polyaxon.schemas.polyflow.schedule import ScheduleSchema
from polyaxon.schemas.specs import kinds


class PipelineSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("pipeline"))
    ops = fields.Nested(OpSchema, many=True)
    templates = fields.Nested("TemplateSchema", many=True)
    schedule = fields.Nested(ScheduleSchema, allow_none=True)
    execute_at = fields.LocalDateTime(allow_none=True)
    init = None
    mounts = None

    @staticmethod
    def schema_config():
        return PipelineConfig


class PipelineConfig(BaseOpConfig):
    SCHEMA = PipelineSchema
    IDENTIFIER = "pipeline"
    REDUCED_ATTRIBUTES = BaseOpConfig.REDUCED_ATTRIBUTES + [
        "ops",
        "templates",
        "schedule",
        "execute_at",
    ]

    def __init__(
        self,
        version=SCHEMA_VERSION,
        kind=IDENTIFIER,
        name=None,
        description=None,
        tags=None,
        profile=None,
        ops=None,
        templates=None,
        environment=None,
        termination=None,
        parallel=None,
        schedule=None,
        execute_at=None,
        inputs=None,
        outputs=None,
    ):
        super(PipelineConfig, self).__init__(
            version=version,
            kind=kind,
            name=name,
            description=description,
            tags=tags,
            profile=profile,
            environment=environment,
            termination=termination,
            parallel=parallel,
            inputs=inputs,
            outputs=outputs,
        )
        self.ops = ops
        self.schedule = schedule
        self.execute_at = execute_at
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
            raise PolyaxonSchemaError(
                "Pipeline has a non valid dag, the dag contains orphan ops: "
                "`{}`".format(orphan_ops)
            )
        self.sort_topologically(dag=dag)

    def _get_op_upstream(self, op):
        upstream = set(op.dependencies) if op.dependencies else set([])

        if not op.params:
            return upstream

        for param in op.params:
            param_ref = ops_params.get_param(
                name=param, value=op.params[param], iotype=None, is_flag=None
            )
            if param_ref and param_ref.entity == ops_params.OPS:
                upstream.add(param_ref.entity_ref)

        return upstream

    def _process_op(self, op):
        upstream = self._get_op_upstream(op=op)
        self._dag = dags.set_dag_op(
            dag=self.dag, op_id=op.name, op=op, upstream=upstream, downstream=None
        )
        for op_name in upstream:
            self._dag = dags.set_dag_op(
                dag=self.dag, op_id=op_name, downstream=[op.name]
            )

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
        return dags.get_independent_ops(self.dag or dag)

    def get_orphan_ops(self, dag=None):
        """Get orphan ops for given dag."""
        return dags.get_orphan_ops(dag or self.dag)

    def sort_topologically(self, dag=None, flatten=False):
        """Sort the dag breath first topologically.

        Only the nodes inside the dag are returned, i.e. the nodes that are also keys.

        Returns:
             a topological ordering of the DAG.
        Raises:
             an error if this is not possible (graph is not valid).
        """

        return dags.sort_topologically(dag or self.dag, flatten=flatten)

    def process_templates(self):
        if not self.templates:
            raise PolyaxonSchemaError(
                "Pipeline is not valid, it has no templates to validate operations."
            )

        if not self.ops:
            raise PolyaxonSchemaError(
                "Pipeline is not valid, it has no ops to validate operations."
            )

        for template in self.templates:
            template_name = template.name
            if template_name in self._template_by_names:
                raise PolyaxonSchemaError(
                    "Pipeline has multiple templates with the same name `{}`".format(
                        template_name
                    )
                )
            self._template_by_names[template_name] = template

        for op in self.ops:
            op_name = op.name
            template_name = op.template.name
            if op_name in self._op_template_mapping:
                raise PolyaxonSchemaError(
                    "Pipeline has multiple ops with the same name `{}`".format(op_name)
                )

            if template_name not in self._template_by_names:
                raise PolyaxonSchemaError(
                    "Pipeline op with name `{}` requires a template with name `{}`, "
                    "which is not defined on this pipeline.".format(
                        op_name, template_name
                    )
                )

            self._op_template_mapping[op_name] = template_name
            outputs = self._template_by_names[template_name].outputs
            if not outputs:
                continue
            for output in outputs:
                self._context["ops.{}.outputs.{}".format(op_name, output.name)] = output

        for op in self.ops:
            template = self._template_by_names[self._op_template_mapping[op.name]]
            ops_params.validate_params(
                params=op.params,
                inputs=template.inputs,
                outputs=template.outputs,
                context=self._context,
                is_template=False,
                check_runs=False,
            )

    def set_op_template(self, op_name):
        if op_name not in self.dag:
            raise PolyaxonSchemaError(
                "Op with name `{}` was not found in Pipeline, "
                "make sure to run `process_dag`.".format(op_name)
            )
        op_spec = self.dag[op_name]
        if op_spec.op._template:
            return
        if op_name not in self._op_template_mapping:
            raise PolyaxonSchemaError(
                "Pipeline op with name `{}` requires a template with name `{}`, "
                "which is not defined on this pipeline, "
                "make sure to run `process_templates`".format(
                    op_name, op_spec.op.template.name
                )
            )
        template_name = self._op_template_mapping[op_name]
        op_spec.op._template = self._template_by_names[template_name]
        # Check version
        if op_spec.op._template.version is None:
            op_spec.op._template.version = self.version
        if op_spec.op.version is None:
            op_spec.op.version = self.version
        # Check op has kind
        if op_spec.op.kind is None:
            op_spec.op.kind = kinds.OPERATION


class TemplateSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        JobConfig.IDENTIFIER: JobSchema,
        ServiceConfig.IDENTIFIER: ServiceSchema,
        PipelineConfig.IDENTIFIER: PipelineSchema,
    }
