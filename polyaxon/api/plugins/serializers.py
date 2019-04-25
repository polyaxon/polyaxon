from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.build import BuildMixin
from api.utils.serializers.data_refs import DataRefsSerializerMixin
from api.utils.serializers.names import NamesMixin
from api.utils.serializers.project import ProjectMixin
from api.utils.serializers.tags import TagsSerializerMixin
from api.utils.serializers.user import UserMixin
from db.models.notebooks import NotebookJob, NotebookJobStatus
from db.models.tensorboards import TensorboardJob, TensorboardJobStatus
from libs.spec_validation import validate_notebook_spec_config, validate_tensorboard_spec_config


class PluginJobBaseSerializer(serializers.ModelSerializer,
                              NamesMixin,
                              BuildMixin,
                              ProjectMixin,
                              UserMixin):
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    build_job = fields.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'user',
            'name',
            'description',
            'project',
            'unique_name',
            'content',
            'pod_id',
            'build_job',
            'last_status',
            'tags',  # Need to implement TagsSerializerMixin
        )

    def _validate_spec(self, content):
        pass

    def validate_content(self, content):
        # content is optional
        if not content:
            return content

        self._validate_spec(content)
        # Resume normal creation
        return content


class TensorboardJobSerializer(PluginJobBaseSerializer):
    def _validate_spec(self, content):
        validate_tensorboard_spec_config(content)

    class Meta(PluginJobBaseSerializer.Meta):
        model = TensorboardJob

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             project=validated_data['project'],
                                             query=TensorboardJob.all)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)


class NotebookJobSerializer(PluginJobBaseSerializer):
    def _validate_spec(self, content):
        validate_notebook_spec_config(content)

    class Meta(PluginJobBaseSerializer.Meta):
        model = NotebookJob
        fields = PluginJobBaseSerializer.Meta.fields + ('data_refs',)

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             project=validated_data['project'],
                                             query=NotebookJob.all)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)


class ProjectTensorboardJobSerializer(serializers.ModelSerializer,
                                      BuildMixin,
                                      ProjectMixin,
                                      UserMixin):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    build_job = fields.SerializerMethodField()

    class Meta:
        model = TensorboardJob
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'pod_id',
            'build_job',
            'node_scheduled',
            'user',
            'description',
            'created_at',
            'updated_at',
            'started_at',
            'finished_at',
            'last_status',
            'tags',
            'project',
            'experiment_group',
            'experiment',
        )


class TensorboardJobDetailSerializer(ProjectTensorboardJobSerializer,
                                     TagsSerializerMixin,
                                     NamesMixin):
    class Meta(ProjectTensorboardJobSerializer.Meta):
        fields = ProjectTensorboardJobSerializer.Meta.fields + (
            'content',
            'description',
            'resources',
            'node_scheduled',
        )

    def get_resources(self, obj):
        return obj.resources.to_dict() if obj.resources else None

    def update(self, instance, validated_data):
        validated_data = self.validated_tags(validated_data=validated_data,
                                             tags=instance.tags)
        validated_data = self.validated_name(validated_data,
                                             project=instance.project,
                                             query=TensorboardJob.all)

        return super().update(instance=instance, validated_data=validated_data)


class ProjectNotebookJobSerializer(serializers.ModelSerializer,
                                   BuildMixin,
                                   ProjectMixin,
                                   UserMixin):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    build_job = fields.SerializerMethodField()

    class Meta:
        model = NotebookJob
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'pod_id',
            'build_job',
            'node_scheduled',
            'user',
            'description',
            'created_at',
            'updated_at',
            'started_at',
            'finished_at',
            'last_status',
            'backend',
            'tags',
            'project',
        )


class NotebookJobDetailSerializer(ProjectNotebookJobSerializer,
                                  DataRefsSerializerMixin,
                                  TagsSerializerMixin,
                                  NamesMixin):
    class Meta(ProjectNotebookJobSerializer.Meta):
        fields = ProjectNotebookJobSerializer.Meta.fields + (
            'content',
            'description',
            'resources',
            'data_refs',
            'node_scheduled',
        )

    def get_resources(self, obj):
        return obj.resources.to_dict() if obj.resources else None

    def update(self, instance, validated_data):
        validated_data = self.validated_tags(validated_data=validated_data,
                                             tags=instance.tags)
        validated_data = self.validated_data_refs(validated_data=validated_data,
                                                  data_refs=instance.data_refs)
        validated_data = self.validated_name(validated_data,
                                             project=instance.project,
                                             query=TensorboardJob.all)

        return super().update(instance=instance, validated_data=validated_data)


class TensorboardJobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = TensorboardJobStatus
        extra_kwargs = {'job': {'read_only': True}}
        exclude = []


class NotebookJobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = NotebookJobStatus
        extra_kwargs = {'job': {'read_only': True}}
        exclude = []
