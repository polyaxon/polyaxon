import pytest
from django.core.exceptions import ValidationError
from django.test import override_settings

from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from tests.utils import BaseTest


@pytest.mark.projects_mark
class TestProjectModel(BaseTest):
    def test_has_code(self):
        project = ProjectFactory()
        self.assertEqual(project.has_code, False)

        RepoFactory(project=project)
        self.assertEqual(project.has_code, True)

    def test_has_owner(self):
        project = ProjectFactory()
        self.assertEqual(project.has_owner, True)

    @override_settings(ALLOW_USER_PROJECTS=False)
    def test_cannot_create(self):
        with self.assertRaises(ValidationError):
            ProjectFactory()
