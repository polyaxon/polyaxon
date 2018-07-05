from collections import namedtuple

from django.contrib.postgres.fields.jsonb import KeyTransform
from django.db import models

from db.models.unique_names import (
    EXPERIMENT_UNIQUE_NAME_FORMAT,
    GROUP_UNIQUE_NAME_FORMAT,
    JOB_UNIQUE_NAME_FORMAT,
    PROJECT_UNIQUE_NAME_FORMAT
)


class OutputsRefsSpec(namedtuple("OutputsRefsSpec", "path persistence")):

    def items(self):
        return self._asdict().items()


def get_paths_from_specs(specs):
    if not specs:
        return None

    return [spec.path for spec in specs]


class OutputsRefs(models.Model):
    jobs = models.ManyToManyField(
        'db.Job',
        blank=True,
        null=True,
        related_name='+')
    experiments = models.ManyToManyField(
        'db.Experiment',
        blank=True,
        null=True,
        related_name='+')

    class Meta:
        app_label = 'db'

    def get_jobs_outputs_spec(self):
        from libs.paths.jobs import get_job_outputs_path

        if not self.jobs.count():
            return None
        annotation = {
            'persistence_outputs': KeyTransform('outputs', 'persistence')
        }
        query = self.jobs.annotate(**annotation)
        job_data = query.values_list('id',
                                     'project__user__username',
                                     'project__name',
                                     'persistence_outputs')
        outputs_spec_data = {}
        for data in job_data:
            project_name = PROJECT_UNIQUE_NAME_FORMAT.format(
                user=data[1],
                project=data[2])
            job_name = JOB_UNIQUE_NAME_FORMAT.format(
                project_name=project_name,
                id=data[0]
            )
            outputs_path = get_job_outputs_path(persistence_outputs=data[3], job_name=job_name)
            outputs_spec_data[data[0]] = OutputsRefsSpec(path=outputs_path, persistence=data[3])

        return outputs_spec_data

    def get_experiments_outputs_spec(self):
        from libs.paths.experiments import get_experiment_outputs_path

        if not self.experiments.count():
            return None
        annotation = {
            'persistence_outputs': KeyTransform('outputs', 'persistence')
        }
        query = self.experiments.annotate(**annotation)
        experiment_data = query.values_list('id',
                                            'experiment_group__id',
                                            'project__user__username',
                                            'project__name',
                                            'persistence_outputs')
        outputs_spec_data = {}
        for data in experiment_data:
            project_name = PROJECT_UNIQUE_NAME_FORMAT.format(
                user=data[2],
                project=data[3])

            if data[1]:
                group_name = GROUP_UNIQUE_NAME_FORMAT.format(
                    project_name=project_name,
                    id=data[1])
                experiment_name = EXPERIMENT_UNIQUE_NAME_FORMAT.format(
                    parent_name=group_name,
                    id=data[0])
            else:
                experiment_name = EXPERIMENT_UNIQUE_NAME_FORMAT.format(
                    parent_name=project_name,
                    id=data[0])
            outputs_path = get_experiment_outputs_path(
                persistence_outputs=data[4],
                experiment_name=experiment_name)
            outputs_spec_data[data[0]] = OutputsRefsSpec(path=outputs_path, persistence=data[4])

        return outputs_spec_data
