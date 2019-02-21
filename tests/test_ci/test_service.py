import os
import shutil

import pytest

import ci

from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from factories.ci_factory import CIFactory
from factories.factory_projects import ProjectFactory
from factories.factory_repos import ExternalRepoFactory, RepoFactory
from libs.repos import git
from tests.utils import BaseTest


@pytest.mark.ci_mark
class TestCIService(BaseTest):

    def setUp(self):
        super().setUp()

        self.project = ProjectFactory()
        # Set ci
        self.ci = CIFactory(project=self.project)

    def test_sync_get_latest_commit_internal_repo(self):
        assert self.ci.code_reference is None
        # No repo
        assert ci.sync(self.project) is False
        assert self.ci.code_reference is None

        # Repo but no commits
        repo = RepoFactory(project=self.project)
        assert ci.sync(self.project) is False
        assert self.ci.code_reference is None

        # Put file and commit
        open('{}/foo'.format(repo.path), 'w')
        git.commit(repo.path, 'user@domain.com', 'username')
        assert ci.sync(self.project) is True
        assert self.ci.code_reference is not None
        last_code_ref = self.ci.code_reference

        # Resync without change does not create new code ref
        assert ci.sync(self.project) is False
        assert self.ci.code_reference == last_code_ref

        # Add new commit
        open('{}/foo2'.format(repo.path), 'w')
        git.commit(repo.path, 'user@domain.com', 'username')
        assert ci.sync(self.project) is True
        assert self.ci.code_reference is not None
        assert self.ci.code_reference != last_code_ref

    def test_sync_get_latest_commit_external_repo(self):
        assert self.ci.code_reference is None
        # No repo
        assert ci.sync(self.project) is False
        assert self.ci.code_reference is None

        # Repo
        repo = ExternalRepoFactory(project=self.project,
                                   git_url='https://github.com/polyaxon/empty.git')
        assert ci.sync(self.project) is True
        assert self.ci.code_reference is not None
        last_code_ref = self.ci.code_reference

        # Resync without change does not create new code ref
        assert ci.sync(self.project) is False
        assert self.ci.code_reference == last_code_ref

        # Creating file manually does not work
        open('{}/foo'.format(repo.path), 'w')
        git.commit(repo.path, 'user@domain.com', 'username')
        assert ci.sync(self.project) is False
        assert self.ci.code_reference is not None
        assert self.ci.code_reference == last_code_ref

    def test_trigger(self):
        assert Experiment.objects.count() == 0
        assert ExperimentGroup.objects.count() == 0
        assert Job.objects.count() == 0
        assert BuildJob.objects.count() == 0

        # No repo
        assert ci.trigger(self.project) is False

        assert Experiment.objects.count() == 0
        assert ExperimentGroup.objects.count() == 0
        assert Job.objects.count() == 0
        assert BuildJob.objects.count() == 0

        # New code
        repo = RepoFactory(project=self.project)
        open('{}/foo'.format(repo.path), 'w')
        git.commit(repo.path, 'user@domain.com', 'username')

        assert ci.trigger(self.project) is False
        assert Experiment.objects.count() == 0
        assert ExperimentGroup.objects.count() == 0
        assert Job.objects.count() == 0
        assert BuildJob.objects.count() == 0

        # New file
        shutil.copy(os.path.abspath('tests/fixtures_static/polyaxonfile.yml'),
                    '{}/polyaxonfile.yml'.format(repo.path))
        git.commit(repo.path, 'user@domain.com', 'username')
        assert ci.trigger(self.project) is True
        assert Experiment.objects.count() == 1
        assert ExperimentGroup.objects.count() == 0
        assert Job.objects.count() == 0
        assert BuildJob.objects.count() == 0
