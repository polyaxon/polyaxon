import pytest

from db.models.ci import CI
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.ci_mark
class TestCIModel(BaseTest):
    def test_project_ci(self):
        project = ProjectFactory()
        self.assertEqual(project.has_ci, False)

        ci = CI.objects.create(project=project)
        self.assertEqual(project.has_ci, True)

        ci.delete()
        project.refresh_from_db()
        self.assertEqual(project.has_ci, False)
