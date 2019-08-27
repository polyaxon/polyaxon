# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six
import warnings

from hestia.list_utils import to_list
from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import DictOrStr
from polyaxon_schemas.ops.environments.outputs import OutputsSchema
from polyaxon_schemas.ops.environments.persistence import PersistenceSchema
from polyaxon_schemas.ops.environments.resources import (
    K8SContainerResourcesConfig,
    PodResourcesConfig,
)


class StoreRefSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    is_managed = fields.Bool(allow_none=True)
    paths = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return StoreRefConfig


class StoreRefConfig(BaseConfig):
    IDENTIFIER = "store_ref"
    SCHEMA = StoreRefSchema
    REDUCED_ATTRIBUTES = ["name", "is_managed", "paths"]

    def __init__(self, name, is_managed=None, paths=None):
        self.name = name
        self.is_managed = is_managed
        self.paths = paths


class K8SResourceRefSchema(BaseSchema):
    name = fields.Str()
    mount_path = fields.Str(allow_none=True)
    items = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return K8SResourceRefConfig


class K8SResourceRefConfig(BaseConfig):
    IDENTIFIER = "k8s_resource_ref"
    SCHEMA = K8SResourceRefSchema
    REDUCED_ATTRIBUTES = ["name", "mount_path", "items"]

    def __init__(self, name, mount_path=None, items=None):
        self.name = name
        self.mount_path = mount_path
        self.items = items


def validate_resource_refs(values, field):
    field_value = values.get(field)
    if not field_value:
        return values
    field_value = [
        {"name": v} if isinstance(v, six.string_types) else v for v in field_value
    ]
    for v in field_value:
        try:
            K8SResourceRefSchema(unknown=BaseConfig.UNKNOWN_BEHAVIOUR).load(v)
        except ValidationError:
            raise ValidationError(
                "K8S Resource field `{}` is not a valid value.".format(v)
            )
    values[field] = field_value
    return values


def validate_config_map_refs(values):
    if values.get("config_map_refs") and values.get("configmap_refs"):
        raise ValidationError("You should only use `config_map_refs`.")

    if values.get("configmap_refs"):
        warnings.warn(
            "The `configmap_refs` parameter is deprecated and will be removed in next release, "
            "please use `config_map_refs` instead.",
            DeprecationWarning,
        )
        values["config_map_refs"] = values.pop("configmap_refs")

    return validate_resource_refs(values=values, field="config_map_refs")


def validate_secret_refs(values):
    return validate_resource_refs(values=values, field="secret_refs")


def validate_persistence(values):
    if values.get("persistence") and (
        values.get("data_refs") or values.get("artifact_refs")
    ):
        raise ValidationError(
            "You cannot use `persistence` and  `data_refs` or `artifact_refs`."
        )

    if values.get("persistence"):
        warnings.warn(
            "The `persistence` parameter is deprecated and will be removed in next release, "
            "please use `data_refs` and/or `artifact_refs` instead.",
            DeprecationWarning,
        )
        persistence = values.pop("persistence")
        values["data_refs"] = to_list(
            values.get("data_refs", persistence.data), check_none=True
        )
        values["artifact_refs"] = to_list(
            values.get("artifact_refs", persistence.outputs), check_none=True
        )
    if values.get("data_refs"):
        artifact_refs = to_list(values.get("artifact_refs", []), check_none=True)
        data_refs = to_list(values.pop("data_refs", []), check_none=True)
        values["artifact_refs"] = artifact_refs + data_refs
    return values


def validate_store_ref(values, field):
    field_value = values.get(field)
    if not field_value:
        return values
    field_value = [
        {"name": v} if isinstance(v, six.string_types) else v for v in field_value
    ]
    for v in field_value:
        try:
            StoreRefSchema(unknown=BaseConfig.UNKNOWN_BEHAVIOUR).load(v)
        except ValidationError:
            raise ValidationError("Persistence field `{}` is not value.".format(v))
    values[field] = field_value
    return values


def validate_artifact_refs(values):
    return validate_store_ref(values, "artifact_refs")


def validate_outputs(values):
    outputs = values.pop("outputs", None)
    if outputs:
        warnings.warn(
            "The `outputs` parameter is deprecated and will be removed in next release, "
            "please notice that it will be ignored.",
            DeprecationWarning,
        )


def validate_resources(values):
    resources = values.pop("resources", None)
    if not resources:
        return values

    try:  # Check deprecated resources
        resources = PodResourcesConfig.from_dict(resources)
        warnings.warn(
            "The `resources` parameter should specify a k8s valid format.",
            DeprecationWarning,
        )
        values["resources"] = K8SContainerResourcesConfig.from_resources_entry(
            resources
        )
    except ValidationError:
        values["resources"] = resources

    return values


class EnvironmentSchema(BaseSchema):
    # To indicate which worker/ps index this session config belongs to
    index = fields.Int(allow_none=True)
    resources = fields.Dict(allow_none=True)
    labels = fields.Dict(allow_none=True)
    annotations = fields.Dict(allow_none=True)
    node_selector = fields.Dict(allow_none=True)
    affinity = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(), allow_none=True)
    service_account = fields.Str(allow_none=True)
    image_pull_secrets = fields.List(fields.Str(), allow_none=True)
    max_restarts = fields.Int(allow_none=True)  # Deprecated
    max_retries = fields.Int(allow_none=True)
    restart_policy = fields.Str(allow_none=True)
    ttl = fields.Int(allow_none=True)
    timeout = fields.Int(allow_none=True)
    env_vars = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)), allow_none=True
    )
    secret_refs = fields.List(DictOrStr(), allow_none=True)
    config_map_refs = fields.List(DictOrStr(), allow_none=True)
    configmap_refs = fields.List(fields.Str(), allow_none=True)  # Deprecated
    data_refs = fields.List(
        DictOrStr(), allow_none=True
    )  # Deprecated, use artifacts with readonly
    artifact_refs = fields.List(DictOrStr(), allow_none=True)
    outputs = fields.Nested(OutputsSchema, allow_none=True)  # Deprecated
    persistence = fields.Nested(PersistenceSchema, allow_none=True)  # Deprecated
    security_context = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return EnvironmentConfig

    @validates_schema
    def validate_config_map_refs(self, values):
        validate_config_map_refs(values)

    @validates_schema
    def validate_secret_refs(self, values):
        validate_secret_refs(values)

    @validates_schema
    def validate_persistence(self, values):
        validate_persistence(values)
        validate_artifact_refs(values)

    @validates_schema
    def validate_resources(self, values):
        validate_resources(values)

    @validates_schema
    def validate_outputs(self, values):
        validate_outputs(values)


class EnvironmentConfig(BaseConfig):
    """
    Pod environment config.

    Args:
        index: `int | None`. The index of the pod.
        resources: `PodResourcesConfig`.
        node_selector: `dict`.
        affinity: `dict`.
        tolerations: `list(dict)`.
    """

    IDENTIFIER = "environment"
    SCHEMA = EnvironmentSchema
    REDUCED_ATTRIBUTES = [
        "index",
        "resources",
        "labels",
        "annotations",
        "node_selector",
        "affinity",
        "tolerations",
        "service_account",
        "image_pull_secrets",
        "max_retries",
        "timeout",
        "restart_policy",
        "ttl",
        "env_vars",
        "secret_refs",
        "config_map_refs",
        "artifact_refs",
        "security_context",
    ]

    def __init__(
        self,
        index=None,
        resources=None,
        labels=None,
        annotations=None,
        node_selector=None,
        affinity=None,
        tolerations=None,
        service_account=None,
        image_pull_secrets=None,
        max_restarts=None,
        max_retries=None,
        timeout=None,
        restart_policy=None,
        ttl=None,
        env_vars=None,
        secret_refs=None,
        config_map_refs=None,
        configmap_refs=None,
        data_refs=None,
        artifact_refs=None,
        persistence=None,
        outputs=None,
        security_context=None,
    ):
        if max_restarts:
            warnings.warn(
                "The `max_restarts` is deprecated and has no effect, please use `max_retries`.",
                DeprecationWarning,
            )
        self.index = index
        self.resources = validate_resources({"resources": resources}).get("resources")
        self.labels = labels
        self.annotations = annotations
        self.node_selector = node_selector
        self.affinity = affinity
        self.tolerations = tolerations
        self.service_account = service_account
        self.image_pull_secrets = image_pull_secrets
        self.max_retries = max_retries
        self.timeout = timeout
        self.restart_policy = restart_policy
        self.ttl = ttl
        self.env_vars = env_vars

        self.secret_refs = validate_secret_refs({"secret_refs": secret_refs}).get(
            "secret_refs"
        )
        self.config_map_refs = validate_config_map_refs(
            {"config_map_refs": config_map_refs, "configmap_refs": configmap_refs}
        ).get("config_map_refs")

        persistence_values = validate_persistence(
            {
                "persistence": persistence,
                "data_refs": data_refs,
                "artifact_refs": artifact_refs,
            }
        )
        self.artifact_refs = validate_artifact_refs(persistence_values).get(
            "artifact_refs"
        )
        validate_outputs({"outputs": outputs})
        self.security_context = security_context
