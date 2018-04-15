from unittest.mock import patch

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, tag
from django.test.client import MULTIPART_CONTENT
from polyaxon_schemas.matrix import MatrixConfig
from polyaxon_schemas.polyaxonfile.specification import GroupSpecification
from polyaxon_schemas.settings import SettingsConfig
from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.models import ExperimentGroup
from experiments.models import Experiment, ExperimentMetric
from experiments.statuses import ExperimentLifeCycle
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory, ExperimentStatusFactory
from factories.factory_projects import ProjectFactory
from factories.fixtures import experiment_group_spec_content_early_stopping
from polyaxon.urls import API_V1
from runner.tasks.experiment_groups import stop_group_experiments
from tests.utils import RUNNER_TEST, BaseTest, BaseViewTest


class TestExperimentGroupModel(BaseTest):
    @override_settings(DEPLOY_RUNNER=False)
    @patch('experiment_groups.paths.delete_path')
    def test_experiment_group_creation_deletes_old_data(self, delete_path):
        ExperimentGroupFactory()

        assert delete_path.call_count == 2  # outputs + logs

    @override_settings(DEPLOY_RUNNER=False)
    @patch('experiment_groups.paths.delete_path')
    def test_experiment_group_deletion_deletes_old_data(self, delete_path):
        experiment_group = ExperimentGroupFactory()
        assert delete_path.call_count == 2  # outputs + logs
        experiment_group.delete()
        assert delete_path.call_count == 2 + 2  # outputs + logs

    @override_settings(DEPLOY_RUNNER=False)
    def test_experiment_group_without_spec_and_pramas(self):
        # Create group without params and spec works
        project = ProjectFactory()
        experiment_group = ExperimentGroup.objects.create(
            user=project.user,
            project=project)
        assert experiment_group.specification is None
        assert experiment_group.params is None
        assert experiment_group.params_config is None
        assert experiment_group.concurrency is None
        assert experiment_group.search_algorithm is None
        assert experiment_group.early_stopping is None

    @override_settings(DEPLOY_RUNNER=False)
    def test_experiment_group_with_spec_create_params(self):
        # Create group with spec creates params
        project = ProjectFactory()
        experiment_group = ExperimentGroup.objects.create(
            user=project.user,
            project=project,
            content=experiment_group_spec_content_early_stopping)
        assert isinstance(experiment_group.specification, GroupSpecification)
        assert experiment_group.params == experiment_group.specification.settings.to_dict()
        assert isinstance(experiment_group.params_config, SettingsConfig)
        assert experiment_group.concurrency == 2
        assert experiment_group.search_algorithm == SearchAlgorithms.RANDOM
        assert len(experiment_group.early_stopping) == 2

    @override_settings(DEPLOY_RUNNER=False)
    def test_experiment_group_with_params(self):
        # Create group with spec creates params
        project = ProjectFactory()
        params = {
            'concurrent_experiments': 2,
            'random_search': {'n_experiments': 10},
            'matrix': {'lr': {'values': [1, 2, 3]}}
        }
        experiment_group = ExperimentGroup.objects.create(
            user=project.user,
            project=project,
            params=params)

        assert experiment_group.specification is None
        assert experiment_group.params == params
        assert isinstance(experiment_group.params_config, SettingsConfig)
        assert experiment_group.concurrency == 2
        assert experiment_group.search_algorithm == SearchAlgorithms.RANDOM
        assert experiment_group.params_config.random_search.n_experiments == 10
        assert isinstance(experiment_group.params_config.matrix['lr'], MatrixConfig)

    @tag(RUNNER_TEST)
    def test_spec_creation_triggers_experiments_planning(self):
        with patch(
            'runner.tasks.experiment_groups.create_group_experiments.apply_async'
        ) as mock_fct:
            experiment_group = ExperimentGroupFactory()

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 0
        assert mock_fct.call_count == 1

    @tag(RUNNER_TEST)
    def test_spec_creation_triggers_experiments_creations_and_scheduling(self):
        with patch('runner.hp_search.grid.hp_grid_search_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory()

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 2
        assert mock_fct.call_count == 1
        assert experiment_group.pending_experiments.count() == 2
        assert experiment_group.running_experiments.count() == 0
        experiment = Experiment.objects.filter(experiment_group=experiment_group).first()
        ExperimentStatusFactory(experiment=experiment, status=ExperimentLifeCycle.RUNNING)
        assert experiment_group.pending_experiments.count() == 1
        assert experiment_group.running_experiments.count() == 1

    @tag(RUNNER_TEST)
    def test_experiment_group_deletion_triggers_experiments_deletion(self):
        with patch('runner.hp_search.grid.hp_grid_search_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory()

        assert mock_fct.call_count == 1

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 2

        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as mock_fct:
            experiment_group.delete()

        assert mock_fct.call_count == 2

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 0

    @tag(RUNNER_TEST)
    def test_experiment_create_a_max_of_experiments(self):
        with patch('runner.hp_search.random.hp_random_search_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_early_stopping)

        assert mock_fct.call_count == 1
        assert experiment_group.specification.matrix_space == 3
        assert experiment_group.experiments.count() == 2

    @tag(RUNNER_TEST)
    def test_experiment_group_should_stop_early(self):
        with patch('runner.hp_search.random.hp_random_search_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_early_stopping)

        assert mock_fct.call_count == 1
        assert experiment_group.should_stop_early() is False
        assert experiment_group.pending_experiments.count() == 2

        # Make a metric for one of the experiments
        experiment1, experiment2 = list(experiment_group.experiments.all())
        metric1 = ExperimentMetric.objects.create(experiment=experiment1,
                                                  values={'precision': 0.99})

        # Check again that early stopping works
        assert experiment_group.should_stop_early() is True

        # Add another metric
        metric2 = ExperimentMetric.objects.create(experiment=experiment2,
                                                  values={'loss': 0.01})

        # Check again that early stopping still works
        assert experiment_group.should_stop_early() is True

        # Delete metric1
        metric1.delete()

        # Check again that early stopping still works
        assert experiment_group.should_stop_early() is True

        # Delete metric2
        metric2.delete()

        # Check again that early stopping still works
        assert experiment_group.should_stop_early() is False

    @tag(RUNNER_TEST)
    def test_stop_pending_experiments(self):
        with patch('runner.hp_search.random.hp_random_search_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_early_stopping)

        assert mock_fct.call_count == 1
        assert experiment_group.pending_experiments.count() == 2

        stop_group_experiments(experiment_group_id=experiment_group.id, pending=True)

        assert experiment_group.pending_experiments.count() == 0

    @tag(RUNNER_TEST)
    def test_stop_all_experiments(self):
        with patch('runner.hp_search.random.hp_random_search_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_early_stopping)

        assert mock_fct.call_count == 1

        # Add a running experiment
        experiment = ExperimentFactory(experiment_group=experiment_group)
        ExperimentStatusFactory(experiment=experiment, status=ExperimentLifeCycle.RUNNING)
        assert experiment_group.pending_experiments.count() == 2
        assert experiment_group.running_experiments.count() == 1
        assert experiment_group.experiments.count() == 3
        assert experiment_group.stopped_experiments.count() == 0

        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as spawner_mock_fct:
            stop_group_experiments(experiment_group_id=experiment_group.id, pending=False)

        assert experiment_group.pending_experiments.count() == 0
        assert experiment_group.running_experiments.count() == 1
        assert spawner_mock_fct.call_count == 1  # Should be stopped with ths function
        assert experiment_group.stopped_experiments.count() == 2


class TestExperimentGroupCommit(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/repo/upload'.format(API_V1,
                                                  self.project.user.username,
                                                  self.project.name)

    @staticmethod
    def get_upload_file(filename='repo'):
        file = File(open('./tests/fixtures_static/{}.tar.gz'.format(filename), 'rb'))
        return SimpleUploadedFile(filename, file.read(),
                                  content_type='multipart/form-data')

    @override_settings(DEPLOY_RUNNER=False)
    def create_experiment_group(self):
        return ExperimentGroupFactory(project=self.project)

    def test_experiment_group_is_saved_with_commit(self):
        uploaded_file = self.get_upload_file()

        self.auth_client.put(self.url,
                             data={'repo': uploaded_file},
                             content_type=MULTIPART_CONTENT)

        last_commit = self.project.repo.last_commit
        assert last_commit is not None

        # Check experiment is created with commit
        experiment_group = self.create_experiment_group()

        assert experiment_group.code_reference.commit == last_commit[0]
        assert experiment_group.code_reference.repo == self.project.repo

        # Make a new upload with repo_new.tar.gz containing 2 files
        new_uploaded_file = self.get_upload_file('updated_repo')
        self.auth_client.put(self.url,
                             data={'repo': new_uploaded_file},
                             content_type=MULTIPART_CONTENT)

        new_commit = self.project.repo.last_commit
        assert new_commit is not None
        assert new_commit[0] != last_commit[0]

        # Check new experiment is created with new commit
        new_experiment_group = self.create_experiment_group()
        assert new_experiment_group.code_reference.commit == new_commit[0]
        assert new_experiment_group.code_reference.repo == self.project.repo

    @tag(RUNNER_TEST)
    def test_check_experiments_have_same_code_reference_as_group(self):
        uploaded_file = self.get_upload_file()

        self.auth_client.put(self.url,
                             data={'repo': uploaded_file},
                             content_type=MULTIPART_CONTENT)

        last_commit = self.project.repo.last_commit
        assert last_commit is not None

        with patch('runner.hp_search.grid.hp_grid_search_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(project=self.project)

        assert mock_fct.call_count == 1
        assert experiment_group.experiments.count() == 2

        assert experiment_group.code_reference is not None

        experiment_code_references = {xp.code_reference
                                      for xp in experiment_group.experiments.all()}
        assert experiment_code_references == {experiment_group.code_reference}
