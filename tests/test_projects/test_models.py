import pytest

from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from tests.utils import BaseTest


@pytest.mark.project
class TestProjectModel(BaseTest):
    def test_has_code(self):
        project = ProjectFactory()
        assert project.has_code is False

        RepoFactory(project=project)
        assert project.has_code is True
