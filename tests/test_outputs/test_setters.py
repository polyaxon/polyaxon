from collections import namedtuple

import pytest
from polyaxon_schemas.environments import OutputsConfig
from rest_framework.exceptions import ValidationError

from db.models.experiments import Experiment
from db.models.jobs import Job
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from signals.outputs import get_valid_ref, get_valid_outputs, set_outputs, set_outputs_refs
from tests.utils import BaseTest


class InstanceSpec(namedtuple("InstanceSpec", "user project")):
    pass


@pytest.mark.outputs_mark
class TestOutputsSetters(BaseTest):
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.project = ProjectFactory(user=self.user)
        self.project_job = JobFactory(project=self.project, name='unique')
        self.job = JobFactory(name='unique2')
        self.project_experiment = ExperimentFactory(project=self.project, name='unique')
        self.experiment = ExperimentFactory(name='unique2')
        self.instance_mock = InstanceSpec(self.user.id, self.project.id)
        self.wrong_instance_mock = InstanceSpec(-1, -1)

    def test_get_valid_ref_by_id(self):
        assert get_valid_ref(
            model=Experiment, entity_id=self.experiment.id)[0] == self.experiment.id
        assert get_valid_ref(
            model=Experiment, entity_id=self.project_experiment.id)[0] == self.project_experiment.id

        assert get_valid_ref(
            model=Job, entity_id=self.job.id)[0] == self.job.id
        assert get_valid_ref(
            model=Job, entity_id=self.project_job.id)[0] == self.project_job.id

        assert get_valid_ref(model=Experiment, entity_id=-1).count() == 0
        assert get_valid_ref(model=Job, entity_id=-1).count() == 0

    def test_get_valid_ref_by_instance_name(self):
        # Valid values
        assert get_valid_ref(
            model=Experiment,
            instance=self.instance_mock,
            entity_args=[self.project_experiment.name])[0] == self.project_experiment.id

        assert get_valid_ref(
            model=Job,
            instance=self.instance_mock,
            entity_args=[self.project_job.name])[0] == self.project_job.id

        # Non valid project and user
        assert get_valid_ref(
            model=Experiment,
            instance=self.wrong_instance_mock,
            entity_args=[self.project_experiment.name]).count() == 0

        assert get_valid_ref(
            model=Job,
            instance=self.wrong_instance_mock,
            entity_args=[self.project_job.name]).count() == 0

        # Non valid values
        assert get_valid_ref(
            model=Experiment,
            instance=self.instance_mock,
            entity_args=[self.experiment.name]).count() == 0

        assert get_valid_ref(
            model=Job,
            instance=self.instance_mock,
            entity_args=[self.job.name]).count() == 0

    def test_get_valid_ref_by_instance_and_project_name(self):
        # Valid values
        assert get_valid_ref(
            model=Experiment,
            instance=self.instance_mock,
            entity_args=[self.project.name,
                         self.project_experiment.name, ])[0] == self.project_experiment.id

        assert get_valid_ref(
            model=Job,
            instance=self.instance_mock,
            entity_args=[self.project.name,
                         self.project_job.name])[0] == self.project_job.id

        # Non valid project and user
        assert get_valid_ref(
            model=Experiment,
            instance=self.wrong_instance_mock,
            entity_args=[self.project.name,
                         self.project_experiment.name]).count() == 0

        assert get_valid_ref(
            model=Job,
            instance=self.wrong_instance_mock,
            entity_args=[self.project.name,
                         self.project_job.name]).count() == 0

        # Non valid values
        assert get_valid_ref(
            model=Experiment,
            instance=self.instance_mock,
            entity_args=[self.project.name,
                         self.experiment.name]).count() == 0

        assert get_valid_ref(
            model=Job,
            instance=self.instance_mock,
            entity_args=[self.project.name,
                         self.job.name]).count() == 0

    def test_get_valid_ref_by_instance_and_project_name_user(self):
        # Valid values
        assert get_valid_ref(
            model=Experiment,
            instance=self.instance_mock,
            entity_args=[self.user.username,
                         self.project.name,
                         self.project_experiment.name])[0] == self.project_experiment.id

        assert get_valid_ref(
            model=Job,
            instance=self.instance_mock,
            entity_args=[self.user.username,
                         self.project.name,
                         self.project_job.name])[0] == self.project_job.id

        # Non valid project and user and all information should pass this time
        assert get_valid_ref(
            model=Experiment,
            instance=self.wrong_instance_mock,
            entity_args=[self.user.username,
                         self.project.name,
                         self.project_experiment.name]).count() == 1

        assert get_valid_ref(
            model=Job,
            instance=self.wrong_instance_mock,
            entity_args=[self.user.username,
                         self.project.name,
                         self.project_job.name]).count() == 1

        # Non valid values
        assert get_valid_ref(
            model=Experiment,
            instance=self.instance_mock,
            entity_args=[self.user.username,
                         self.project.name,
                         self.experiment.name]).count() == 0

        assert get_valid_ref(
            model=Job,
            instance=self.instance_mock,
            entity_args=[self.user.username,
                         self.project.name,
                         self.job.name]).count() == 0

    def test_get_valid_outputs(self):
        # Valid outputs experiments
        outputs = [
            '{}'.format(self.experiment.id),
            '{}'.format(self.project_experiment.id),
            self.project_experiment.name,
            '{}.{}'.format(self.project.name, self.project_experiment.name),
            '{}/{}'.format(self.project.name, self.project_experiment.name),
            '{}.{}.{}'.format(self.user.username, self.project.name, self.project_experiment.name),
            '{}/{}/{}'.format(self.user.username, self.project.name, self.project_experiment.name),
        ]

        assert len(get_valid_outputs(instance=self.instance_mock,
                                     outputs=outputs,
                                     model=Experiment,
                                     entity='Experiment')) == len(outputs)

        # Valid outputs jobs
        outputs = [
            '{}'.format(self.job.id),
            '{}'.format(self.project_job.id),
            self.project_job.name,
            '{}.{}'.format(self.project.name, self.project_job.name),
            '{}/{}'.format(self.project.name, self.project_job.name),
            '{}.{}.{}'.format(self.user.username, self.project.name, self.project_job.name),
            '{}/{}/{}'.format(self.user.username, self.project.name, self.project_job.name),
        ]

        assert len(get_valid_outputs(instance=self.instance_mock,
                                     outputs=outputs,
                                     model=Job,
                                     entity='Job')) == len(outputs)

        # Non valid outputs
        outputs = [
            self.experiment.name,
            '{}.{}'.format(self.project.name, self.experiment.name),
            '{}/{}'.format(self.project.name, self.experiment.name),
            '{}.{}.{}'.format(self.user.username, self.project.name, self.experiment.name),
            '{}/{}/{}'.format(self.user.username, self.project.name, self.experiment.name),
        ]
        with self.assertRaises(ValidationError):
            get_valid_outputs(instance=self.instance_mock,
                              outputs=outputs,
                              model=Experiment,
                              entity='Experiment')

        outputs = [
            self.job.name,
            '{}.{}'.format(self.project.name, self.job.name),
            '{}/{}'.format(self.project.name, self.job.name),
            '{}.{}.{}'.format(self.user.username, self.project.name, self.job.name),
            '{}/{}/{}'.format(self.user.username, self.project.name, self.job.name),
        ]
        with self.assertRaises(ValidationError):
            get_valid_outputs(instance=self.instance_mock,
                              outputs=outputs,
                              model=Job,
                              entity='Job')

    def test_set_outputs(self):
        experiment_outputs = [
            '{}'.format(self.experiment.id),
            '{}'.format(self.project_experiment.id),
            self.project_experiment.name,
            '{}.{}'.format(self.project.name, self.project_experiment.name),
            '{}/{}'.format(self.project.name, self.project_experiment.name),
            '{}.{}.{}'.format(self.user.username, self.project.name, self.project_experiment.name),
            '{}/{}/{}'.format(self.user.username, self.project.name, self.project_experiment.name),
        ]
        job_outputs = [
            '{}'.format(self.job.id),
            '{}'.format(self.project_job.id),
            self.project_job.name,
            '{}.{}'.format(self.project.name, self.project_job.name),
            '{}/{}'.format(self.project.name, self.project_job.name),
            '{}.{}.{}'.format(self.user.username, self.project.name, self.project_job.name),
            '{}/{}/{}'.format(self.user.username, self.project.name, self.project_job.name),
        ]
        outputs_config = OutputsConfig(jobs=job_outputs, experiments=experiment_outputs).to_dict()

        experiment = ExperimentFactory(user=self.user, project=self.project)
        assert experiment.outputs is None
        experiment.outputs = outputs_config
        assert experiment.outputs is not None
        assert len(experiment.outputs_experiments) == len(experiment_outputs)
        assert len(experiment.outputs_jobs) == len(job_outputs)
        set_outputs(instance=experiment)
        del experiment.outputs_config
        del experiment.outputs_experiments
        del experiment.outputs_jobs
        assert len(experiment.outputs_experiments) == 2
        assert len(experiment.outputs_jobs) == 2

        job = JobFactory(user=self.user, project=self.project)
        assert job.outputs is None
        job.outputs = outputs_config
        assert job.outputs is not None
        assert job.outputs is not None
        assert len(job.outputs_experiments) == len(experiment_outputs)
        assert len(job.outputs_jobs) == len(job_outputs)
        set_outputs(instance=job)
        del job.outputs_config
        del job.outputs_experiments
        del job.outputs_jobs
        assert len(job.outputs_experiments) == 2
        assert len(job.outputs_jobs) == 2

    def test_set_outputs_refs(self):
        experiment_outputs = [
            '{}'.format(self.experiment.id),
            '{}'.format(self.project_experiment.id),
            self.project_experiment.name,
            '{}.{}'.format(self.project.name, self.project_experiment.name),
            '{}/{}'.format(self.project.name, self.project_experiment.name),
            '{}.{}.{}'.format(self.user.username, self.project.name, self.project_experiment.name),
            '{}/{}/{}'.format(self.user.username, self.project.name, self.project_experiment.name),
        ]
        job_outputs = [
            '{}'.format(self.job.id),
            '{}'.format(self.project_job.id),
            self.project_job.name,
            '{}.{}'.format(self.project.name, self.project_job.name),
            '{}/{}'.format(self.project.name, self.project_job.name),
            '{}.{}.{}'.format(self.user.username, self.project.name, self.project_job.name),
            '{}/{}/{}'.format(self.user.username, self.project.name, self.project_job.name),
        ]
        outputs_config = OutputsConfig(jobs=job_outputs, experiments=experiment_outputs).to_dict()

        experiment = ExperimentFactory(user=self.user, project=self.project)
        assert experiment.outputs_refs is None
        experiment.outputs = outputs_config
        set_outputs(instance=experiment)
        set_outputs_refs(instance=experiment)
        assert experiment.outputs_refs is not None
        assert len(experiment.outputs_refs_jobs) == 2
        assert len(experiment.outputs_refs_experiments) == 2

        job = JobFactory(user=self.user, project=self.project)
        assert job.outputs_refs is None
        job.outputs = outputs_config
        set_outputs(instance=job)
        set_outputs_refs(instance=job)
        assert experiment.outputs_refs is not None
        assert len(experiment.outputs_refs_jobs) == 2
        assert len(experiment.outputs_refs_experiments) == 2
