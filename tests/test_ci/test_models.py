import pytest

from db.models.ci import CI
from factories.factory_code_reference import CodeReferenceFactory
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory, ExternalRepoFactory
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

    def test_create_project_with_ci_code_ref(self):
        project = ProjectFactory()
        repo = RepoFactory(project=project)
        code_ref = CodeReferenceFactory(repo=repo)
        ci = CI.objects.create(project=project, code_reference=code_ref)
        assert ci.code_reference == code_ref

    def test_project_ci_code_ref(self):
        project = ProjectFactory()
        repo = ExternalRepoFactory(project=project, git_url='https://github.com/polyaxon/empty.git')
        ci = CI.objects.create(project=project)
        assert ci.code_reference is None

        code_ref = CodeReferenceFactory(external_repo=repo)
        ci.code_reference = code_ref
        ci.save()
        ci.refresh_from_db()
        assert ci.code_reference == code_ref

        code_ref = CodeReferenceFactory(external_repo=repo)
        ci.code_reference = code_ref
        ci.save()
        ci.refresh_from_db()
        assert ci.code_reference == code_ref
