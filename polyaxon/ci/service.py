import logging

from typing import Optional

from hestia.service_interface import Service

from schemas.polyaxonfile import PolyaxonFile, get_default_polyaxonfile

_logger = logging.getLogger('polyaxon.ci')


class CIService(Service):
    __all__ = ('sync', 'trigger',)

    def sync(self, project: 'Project') -> bool:
        # Check if project has CI enabled
        if not project.has_ci:
            return False

        # Get latest code ref for the project

        from libs.repos.utils import get_code_reference

        code_ref = get_code_reference(project=project)
        if not code_ref:
            return False

        # Compare with CI code ref
        project_ci = project.ci
        if project_ci.code_reference == code_ref:  # Code ref already triggered
            return False

        # Code ref is new to CI, set it up
        project_ci.code_reference = code_ref
        project_ci.save(update_fields=['code_reference'])
        return True

    @staticmethod
    def get_specification(polyaxonfile_path: str) -> Optional['BaseSpecification']:
        if not polyaxonfile_path:
            return

        try:
            plx_file = PolyaxonFile(polyaxonfile_path)
        except Exception as e:
            _logger.warning("Polyaxonfile is not valid.")
            _logger.warning('Error message: %s', e)
            return

        return plx_file.specification

    @staticmethod
    def run_experiment(project: 'Project', specification: 'BaseSpecification') -> None:
        from db.models.experiments import Experiment

        Experiment.objects.create(
            user_id=project.ci.user_id,
            project=project,
            tags=['ci'],
            config=specification.parsed_data,
            code_reference_id=project.ci.code_reference_id
        )

    @staticmethod
    def run_group(project: 'Project', specification: 'BaseSpecification') -> None:
        from db.models.experiment_groups import ExperimentGroup

        ExperimentGroup.objects.create(
            user_id=project.ci.user_id,
            project=project,
            tags=['ci'],
            content=specification._data,  # pylint:disable=protected-access
            code_reference_id=project.ci.code_reference_id
        )

    @staticmethod
    def run_job(project: 'Project', specification: 'BaseSpecification') -> None:
        from db.models.jobs import Job

        Job.objects.create(
            user_id=project.ci.user_id,
            project=project,
            tags=['ci'],
            config=specification.parsed_data,
            code_reference_id=project.ci.code_reference_id
        )

    @staticmethod
    def run_build(project: 'Project', specification: 'BaseSpecification') -> None:
        from db.models.build_jobs import BuildJob

        BuildJob.objects.create(
            user_id=project.ci.user_id,
            project=project,
            tags=['ci'],
            config=specification.parsed_data,
            code_reference_id=project.ci.code_reference_id
        )

    def trigger(self, project: 'Project') -> bool:
        # Sync CI first
        if not project.has_code or not self.sync(project=project):
            return False

        # Get polyaxonfile/ci
        if project.has_external_repo:
            repo_path = project.external_repo.path
        else:
            repo_path = project.repo.path
        polyaxonfile_path = get_default_polyaxonfile(path=repo_path)

        # Get specification
        specification = self.get_specification(polyaxonfile_path)
        if not specification:
            return False

        spec_cond = (specification.is_experiment or
                     specification.is_group or
                     specification.is_job or
                     specification.is_build)
        if not spec_cond:
            _logger.warning(
                'The CI expects an experiment, a group, a job, or a build specification,'
                'received instead a `%s` specification', specification.kind)
            return False

        if specification.is_experiment:
            self.run_experiment(project, specification)
        elif specification.is_group:
            self.run_group(project, specification)
        elif specification.is_job:
            self.run_job(project, specification)
        elif specification.is_build:
            self.run_build(project, specification)

        return True
