import random

from unittest.mock import patch

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, tag
from django.test.client import MULTIPART_CONTENT

from experiment_groups.iteration_managers import BOIterationManager, HyperbandIterationManager
from models.experiment_groups import ExperimentGroup, ExperimentGroupIteration
from experiment_groups.search_managers import (
    BOSearchManager,
    GridSearchManager,
    HyperbandSearchManager,
    RandomSearchManager
)
from statuses.experiment_groups import ExperimentGroupLifeCycle
from experiments.models import Experiment, ExperimentMetric
from statuses.experiments import ExperimentLifeCycle
from factories.factory_experiment_groups import ExperimentGroupFactory, ExperimentGroupStatusFactory
from factories.factory_experiments import ExperimentFactory, ExperimentStatusFactory
from factories.factory_projects import ProjectFactory
from factories.fixtures import (
    experiment_group_spec_content_bo,
    experiment_group_spec_content_early_stopping,
    experiment_group_spec_content_hyperband,
    experiment_group_spec_content_hyperband_trigger_reschedule
)
from polyaxon.urls import API_V1
from polyaxon_schemas.matrix import MatrixConfig
from polyaxon_schemas.polyaxonfile.specification import GroupSpecification
from polyaxon_schemas.settings import SettingsConfig
from polyaxon_schemas.utils import SearchAlgorithms
from runner.hp_search.bo import hp_bo_start
from runner.hp_search.hyperband import hp_hyperband_start
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
            'concurrency': 2,
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

    @override_settings(DEPLOY_RUNNER=False)
    def test_iteration(self):
        experiment_group = ExperimentGroupFactory()
        assert experiment_group.iteration is None
        assert experiment_group.iteration_data is None

        # Add iteration
        iteration = ExperimentGroupIteration.objects.create(
            experiment_group=experiment_group,
            data={'dummy': 10})

        assert experiment_group.iteration == iteration
        assert experiment_group.iteration_data == {'dummy': 10}

        # Update data
        iteration.data['foo'] = 'bar'
        iteration.save()

        assert experiment_group.iteration.data == {'dummy': 10, 'foo': 'bar'}

    @override_settings(DEPLOY_RUNNER=False)
    def test_should_stop_early(self):
        # Experiment group with no early stopping
        experiment_group = ExperimentGroupFactory()
        assert experiment_group.should_stop_early() is False

        # Experiment group with early stopping
        experiment_group = ExperimentGroupFactory(
            content=None,
            params={
                'concurrency': 2,
                'random_search': {'n_experiments': 10},
                'early_stopping': [
                    {'metric': 'precision',
                     'value': 0.9,
                     'optimization': 'maximize'}
                ],
                'matrix': {'lr': {'values': [1, 2, 3]}}
            })
        assert experiment_group.should_stop_early() is False

        # Create experiments and metrics
        experiments = [ExperimentFactory(experiment_group=experiment_group) for _ in range(2)]
        ExperimentMetric.objects.create(experiment=experiments[0], values={'precision': 0.8})

        assert experiment_group.should_stop_early() is False

        # Create a metric that triggers early stopping
        ExperimentMetric.objects.create(experiment=experiments[0], values={'precision': 0.91})

        assert experiment_group.should_stop_early() is True

    @override_settings(DEPLOY_RUNNER=False)
    def test_get_ordered_experiments_by_metric(self):
        experiment_group = ExperimentGroupFactory()

        assert len(  # pylint:disable=len-as-condition
            experiment_group.get_ordered_experiments_by_metric(
                experiment_ids=[],
                metric='precision',
                optimization='maximize'
            )) == 0

        experiments = []
        experiment_ids = []
        for _ in range(5):
            experiment = ExperimentFactory(experiment_group=experiment_group)
            experiments.append(experiment)
            experiment_ids.append(experiment.id)
            ExperimentMetric.objects.create(experiment=experiment,
                                            values={'precision': random.random()})

        for experiment in experiments[:3]:
            ExperimentMetric.objects.create(experiment=experiment,
                                            values={'loss': random.random()})

        experiment_metrics = experiment_group.get_ordered_experiments_by_metric(
            experiment_ids=experiment_ids,
            metric='precision',
            optimization='maximize'
        )

        assert len(experiment_metrics) == 5
        metrics = [m.precision for m in experiment_metrics if m.precision is not None]
        assert len(metrics) == 2
        assert sorted(metrics, reverse=True) == metrics

        experiment_metrics = experiment_group.get_ordered_experiments_by_metric(
            experiment_ids=experiment_ids,
            metric='loss',
            optimization='minimize'
        )
        assert len(experiment_metrics) == 5
        metrics = [m.loss for m in experiment_metrics if m.loss is not None]
        assert len(metrics) == 3
        assert sorted(metrics) == metrics

        experiment_metrics = experiment_group.get_ordered_experiments_by_metric(
            experiment_ids=experiment_ids,
            metric='accuracy',
            optimization='maximize'
        )

        assert len(experiment_metrics) == 5  # pylint:disable=len-as-condition
        assert len(  # pylint:disable=len-as-condition
            [m for m in experiment_metrics if m.accuracy is not None]) == 0

    @override_settings(DEPLOY_RUNNER=False)
    def test_get_experiments_metrics(self):
        experiment_group = ExperimentGroupFactory()

        assert len(experiment_group.get_experiments_metrics(  # pylint:disable=len-as-condition
            experiment_ids=[],
            metric='precision'
        )) == 0

        experiments = []
        experiment_ids = []
        for _ in range(5):
            experiment = ExperimentFactory(experiment_group=experiment_group)
            experiments.append(experiment)
            experiment_ids.append(experiment.id)
            ExperimentMetric.objects.create(experiment=experiment,
                                            values={'precision': random.random()})

        for experiment in experiments[:3]:
            ExperimentMetric.objects.create(experiment=experiment,
                                            values={'loss': random.random()})

        experiment_metrics = experiment_group.get_experiments_metrics(
            experiment_ids=experiment_ids,
            metric='precision'
        )

        assert len(experiment_metrics) == 5
        metrics = [m[1] for m in experiment_metrics if m[1] is not None]
        assert len(metrics) == 2

        experiment_metrics = experiment_group.get_experiments_metrics(
            experiment_ids=experiment_ids,
            metric='loss'
        )
        assert len(experiment_metrics) == 5
        metrics = [m[1] for m in experiment_metrics if m[1] is not None]
        assert len(metrics) == 3

        experiment_metrics = experiment_group.get_experiments_metrics(
            experiment_ids=experiment_ids,
            metric='accuracy'
        )

        assert len(experiment_metrics) == 5
        assert len(  # pylint:disable=len-as-condition
            [m for m in experiment_metrics if m[1] is not None]) == 0

    @override_settings(DEPLOY_RUNNER=False)
    def test_managers(self):
        experiment_group = ExperimentGroupFactory(content=None, params=None)
        assert experiment_group.search_manager is None

        # Adding params
        experiment_group.params = {
            'concurrency': 2,
            'grid_search': {'n_experiments': 10},
            'matrix': {'lr': {'values': [1, 2, 3]}}
        }
        experiment_group.save()
        experiment_group = ExperimentGroup.objects.get(id=experiment_group.id)
        assert isinstance(experiment_group.search_manager, GridSearchManager)
        assert experiment_group.iteration_manager is None

        # Adding params
        experiment_group.params = {
            'concurrency': 2,
            'random_search': {'n_experiments': 10},
            'matrix': {'lr': {'values': [1, 2, 3]}}
        }
        experiment_group.save()
        experiment_group = ExperimentGroup.objects.get(id=experiment_group.id)
        assert isinstance(experiment_group.search_manager, RandomSearchManager)
        assert experiment_group.iteration_manager is None

        # Adding params
        experiment_group.params = {
            'concurrency': 2,
            'hyperband': {
                'max_iter': 10,
                'eta': 3,
                'resource': {'name': 'steps', 'type': 'int'},
                'resume': False,
                'metric': {'name': 'loss', 'optimization': 'minimize'}
            },
            'matrix': {'lr': {'values': [1, 2, 3]}}
        }
        experiment_group.save()
        experiment_group = ExperimentGroup.objects.get(id=experiment_group.id)
        assert isinstance(experiment_group.search_manager, HyperbandSearchManager)
        assert isinstance(experiment_group.iteration_manager, HyperbandIterationManager)

        # Adding params
        experiment_group.params = {
            'concurrency': 2,
            'bo': {
                'n_iterations': 4,
                'n_initial_trials': 4,
                'metric': {
                    'name': 'loss',
                    'optimization': 'minimize'
                },
                'utility_function': {
                    'acquisition_function': 'ei',
                    'eps': 1.2,
                    'gaussian_process': {
                        'kernel': 'matern',
                        'length_scale': 1.0,
                        'nu': 1.9,
                        'n_restarts_optimizer': 0
                    }
                }
            },
            'matrix': {'lr': {'values': [1, 2, 3]}}
        }
        experiment_group.save()
        experiment_group = ExperimentGroup.objects.get(id=experiment_group.id)
        assert isinstance(experiment_group.search_manager, BOSearchManager)
        assert isinstance(experiment_group.iteration_manager, BOIterationManager)

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
        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as _:  # noqa
            ExperimentStatusFactory(experiment=experiment, status=ExperimentLifeCycle.SUCCEEDED)
        assert experiment_group.pending_experiments.count() == 1
        assert experiment_group.running_experiments.count() == 0
        assert experiment_group.succeeded_experiments.count() == 1
        experiment.resume()
        assert experiment_group.pending_experiments.count() == 2
        assert experiment_group.running_experiments.count() == 0
        assert experiment_group.succeeded_experiments.count() == 1

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

    @tag(RUNNER_TEST)
    def test_stopping_group_stops_iteration(self):
        # Fake reschedule
        with patch('runner.hp_search.hyperband.hp_hyperband_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_hyperband_trigger_reschedule)
        assert mock_fct.call_count == 1
        ExperimentGroupIteration.objects.create(
            experiment_group=experiment_group,
            data={
                'iteration': 0,
                'bracket_iteration': 21
            })
        # Mark experiment as done
        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as _:  # noqa
            for xp in experiment_group.experiments.all():
                ExperimentStatusFactory(experiment=xp, status=ExperimentLifeCycle.SUCCEEDED)
        # Mark group as stopped
        ExperimentGroupStatusFactory(experiment_group=experiment_group,
                                     status=ExperimentGroupLifeCycle.STOPPED)
        with patch('runner.hp_search.hyperband.hp_hyperband_create.delay') as mock_fct1:
            hp_hyperband_start(experiment_group.id)

        assert mock_fct1.call_count == 0

    @tag(RUNNER_TEST)
    def test_hyperband_rescheduling(self):
        with patch('runner.hp_search.hyperband.hp_hyperband_start.apply_async') as mock_fct:
            ExperimentGroupFactory(content=experiment_group_spec_content_hyperband)

        assert mock_fct.call_count == 1

        with patch('runner.hp_search.hyperband.hp_hyperband_iterate.delay') as mock_fct1:
            with patch('runner.tasks.experiments.build_experiment.delay') as mock_fct2:
                ExperimentGroupFactory(
                    content=experiment_group_spec_content_hyperband_trigger_reschedule)

        assert mock_fct1.call_count == 1
        assert mock_fct2.call_count == 9

        # Fake reschedule
        with patch('runner.hp_search.hyperband.hp_hyperband_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_hyperband_trigger_reschedule)
        assert mock_fct.call_count == 1
        ExperimentGroupIteration.objects.create(
            experiment_group=experiment_group,
            data={
                'iteration': 0,
                'bracket_iteration': 21
            })

        # Mark experiment as done
        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as _:  # noqa
            for xp in experiment_group.experiments.all():
                ExperimentStatusFactory(experiment=xp, status=ExperimentLifeCycle.SUCCEEDED)
        with patch('runner.hp_search.hyperband.hp_hyperband_create.delay') as mock_fct1:
            hp_hyperband_start(experiment_group.id)

        assert mock_fct1.call_count == 1

        # Fake reduce
        with patch('runner.hp_search.hyperband.hp_hyperband_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_hyperband_trigger_reschedule)
        assert mock_fct.call_count == 1
        assert experiment_group.non_done_experiments.count() == 9

        # Mark experiment as done
        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as _:  # noqa
            for xp in experiment_group.experiments.all():
                ExperimentStatusFactory(experiment=xp, status=ExperimentLifeCycle.SUCCEEDED)
        with patch('runner.hp_search.hyperband.hp_hyperband_start.apply_async') as mock_fct2:
            with patch.object(HyperbandIterationManager, 'reduce_configs') as mock_fct3:
                hp_hyperband_start(experiment_group.id)
        assert mock_fct2.call_count == 1
        assert mock_fct3.call_count == 1

    @tag(RUNNER_TEST)
    def test_bo_rescheduling(self):
        with patch('runner.hp_search.bo.hp_bo_start.apply_async') as mock_fct:
            ExperimentGroupFactory(content=experiment_group_spec_content_bo)

        assert mock_fct.call_count == 1

        with patch('runner.hp_search.bo.hp_bo_iterate.delay') as mock_fct1:
            with patch('runner.tasks.experiments.build_experiment.delay') as mock_fct2:
                ExperimentGroupFactory(
                    content=experiment_group_spec_content_bo)

        assert mock_fct1.call_count == 1
        assert mock_fct2.call_count == 2

        # Fake
        with patch('runner.hp_search.bo.hp_bo_start.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_bo)
        assert mock_fct.call_count == 1
        assert experiment_group.non_done_experiments.count() == 2

        # Mark experiment as done
        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as _:  # noqa
            for xp in experiment_group.experiments.all():
                ExperimentStatusFactory(experiment=xp, status=ExperimentLifeCycle.SUCCEEDED)
        with patch('runner.hp_search.bo.hp_bo_iterate.delay') as mock_fct1:
            hp_bo_start(experiment_group.id)
        assert mock_fct1.call_count == 1

        # Mark experiment as done
        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as _:  # noqa
            for xp in experiment_group.experiments.all():
                ExperimentStatusFactory(experiment=xp, status=ExperimentLifeCycle.SUCCEEDED)
        with patch('runner.hp_search.bo.hp_bo_create.delay') as mock_fct1:
            hp_bo_start(experiment_group.id)
        assert mock_fct1.call_count == 1


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
