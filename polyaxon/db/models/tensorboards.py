from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from db.models.abstract_jobs import AbstractJobStatus, JobMixin
from db.models.plugins import PluginJobBase
from libs.spec_validation import validate_tensorboard_spec_config
from polyaxon_schemas.polyaxonfile.specification import TensorboardSpecification


class TensorboardJob(PluginJobBase, JobMixin):
    """A model that represents the configuration for tensorboard job."""
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs')
    config = JSONField(
        help_text='The compiled polyaxonfile for the tensorboard job.',
        validators=[validate_tensorboard_spec_config])
    experiment_group = models.ForeignKey(
        'db.ExperimentGroup',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs',
        null=True,
        blank=True)
    experiment = models.ForeignKey(
        'db.Experiment',
        on_delete=models.CASCADE,
        related_name='tensorboard_jobs',
        null=True,
        blank=True)
    status = models.OneToOneField(
        'db.TensorboardJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True,
        on_delete=models.SET_NULL)

    class Meta:
        app_label = 'db'

    @cached_property
    def unique_name(self):
        return '{}.tensorboards.{}'.format(self.project.unique_name, self.id)

    @cached_property
    def specification(self):
        return TensorboardSpecification(values=self.config)

    def set_status(self, status, message=None, details=None):  # pylint:disable=arguments-differ
        return self._set_status(status_model=TensorboardJobStatus,
                                status=status,
                                message=message,
                                details=details)

    @cached_property
    def outputs_path(self):
        if self.experiment:
            from libs.paths.experiments import get_experiment_outputs_path
            return get_experiment_outputs_path(
                persistence_outputs=self.experiment.persistence_outputs,
                experiment_name=self.experiment.unique_name,
                original_name=self.experiment.original_unique_name,
                cloning_strategy=self.experiment.cloning_strategy)
        if self.experiment_group:
            from libs.paths.experiment_groups import get_experiment_group_outputs_path
            return get_experiment_group_outputs_path(
                persistence_outputs=self.experiment_group.persistence_outputs,
                experiment_group_name=self.experiment_group.unique_name)

        from libs.paths.projects import get_project_outputs_path
        return get_project_outputs_path(persistence_outputs=None,
                                        project_name=self.project.unique_name)


class TensorboardJobStatus(AbstractJobStatus):
    """A model that represents tensorboard job status at certain time."""
    job = models.ForeignKey(
        'db.TensorboardJob',
        on_delete=models.CASCADE,
        related_name='statuses')

    class Meta(AbstractJobStatus.Meta):
        app_label = 'db'
        verbose_name_plural = 'Tensorboard Job Statuses'
