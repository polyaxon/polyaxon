import pytest

from crons.tasks.deletion import (
    delete_archived_build_jobs,
    delete_archived_experiment_groups,
    delete_archived_experiments,
    delete_archived_jobs,
    delete_archived_notebook_jobs,
    delete_archived_projects,
    delete_archived_tensorboard_jobs
)
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from polyaxon.config_settings import CleaningIntervals
from tests.utils import BaseTest


@pytest.mark.crons_mark
class TestDeletionCrons(BaseTest):
    def test_delete_projects(self):
        project1 = ProjectFactory()
        ExperimentFactory(project=project1)
        project1.archive()
        project2 = ProjectFactory()
        experiment2 = ExperimentFactory(project=project2)
        experiment2.archive()

        assert Project.all.count() == 2
        assert Experiment.all.count() == 2

        CleaningIntervals.ARCHIVED = -10
        delete_archived_projects()

        # Deletes only one project
        assert Project.all.count() == 1
        # Although the other experiment is archived it's not deleted because of project2
        assert Experiment.all.count() == 1

    def test_delete_experiment_groups(self):
        project1 = ProjectFactory()
        ExperimentGroupFactory(project=project1)
        project1.archive()
        project2 = ProjectFactory()
        experiment_group2 = ExperimentGroupFactory(project=project2)
        experiment_group2.archive()

        assert ExperimentGroup.all.count() == 2

        CleaningIntervals.ARCHIVED = -10
        delete_archived_experiment_groups()

        # Although the other entity is archived it's not deleted because of project1
        assert ExperimentGroup.all.count() == 1

    def test_delete_experiments(self):
        project1 = ProjectFactory()
        ExperimentFactory(project=project1)
        project1.archive()
        project2 = ProjectFactory()
        experiment2 = ExperimentFactory(project=project2)
        experiment2.archive()
        group1 = ExperimentGroupFactory()
        experiment3 = ExperimentFactory(experiment_group=group1)
        experiment3.archive()

        assert Experiment.all.count() == 3

        CleaningIntervals.ARCHIVED = -10
        delete_archived_experiments()

        # Although the other experiment is archived it's not deleted because of project1 and group1
        assert Experiment.all.count() == 2

    def test_delete_jobs(self):
        project1 = ProjectFactory()
        JobFactory(project=project1)
        project1.archive()
        project2 = ProjectFactory()
        job2 = JobFactory(project=project2)
        job2.archive()

        assert Job.all.count() == 2

        CleaningIntervals.ARCHIVED = -10
        delete_archived_jobs()

        # Although the other entity is archived it's not deleted because of project1
        assert Job.all.count() == 1

    def test_delete_build_jobs(self):
        project1 = ProjectFactory()
        BuildJobFactory(project=project1)
        project1.archive()
        project2 = ProjectFactory()
        job2 = BuildJobFactory(project=project2)
        job2.archive()

        assert BuildJob.all.count() == 2

        CleaningIntervals.ARCHIVED = -10
        delete_archived_build_jobs()

        # Although the other entity is archived it's not deleted because of project1
        assert BuildJob.all.count() == 1

    def test_delete_notebook_jobs(self):
        project1 = ProjectFactory()
        NotebookJobFactory(project=project1)
        project1.archive()
        project2 = ProjectFactory()
        job2 = NotebookJobFactory(project=project2)
        job2.archive()

        assert NotebookJob.all.count() == 2

        CleaningIntervals.ARCHIVED = -10
        delete_archived_notebook_jobs()

        # Although the other entity is archived it's not deleted because of project1
        assert NotebookJob.all.count() == 1

    def test_delete_tensorboard_jobs(self):
        project1 = ProjectFactory()
        TensorboardJobFactory(project=project1)
        project1.archive()
        project2 = ProjectFactory()
        job2 = TensorboardJobFactory(project=project2)
        job2.archive()

        assert TensorboardJob.all.count() == 2

        CleaningIntervals.ARCHIVED = -10
        delete_archived_tensorboard_jobs()

        # Although the other entity is archived it's not deleted because of project1
        assert TensorboardJob.all.count() == 1
