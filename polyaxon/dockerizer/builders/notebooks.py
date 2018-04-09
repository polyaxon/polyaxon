import logging

from dockerizer.builders.jobs import BaseJobDockerBuilder, build_job
from projects.models import Project

logger = logging.getLogger('polyaxon.dockerizer.builders')


class NotebookDockerBuilder(BaseJobDockerBuilder):
    def __init__(self,
                 project_id,
                 project_name,
                 repo_path,
                 from_image,
                 image_name,
                 image_tag,
                 copy_code=False,
                 in_tmp_repo=False,
                 steps=None,
                 env_vars=None,
                 dockerfile_name='Dockerfile'):
        super(NotebookDockerBuilder, self).__init__(
            project_id=project_id,
            project_name=project_name,
            repo_path=repo_path,
            from_image=from_image,
            image_name=image_name,
            image_tag=image_tag,
            copy_code=copy_code,
            in_tmp_repo=in_tmp_repo,
            steps=steps,
            env_vars=env_vars,
            dockerfile_name=dockerfile_name)

    def _check_pulse(self, check_pulse):
        check_pulse += 1
        # Check if experiment is not stopped in the meanwhile
        if check_pulse > self.CHECK_INTERVAL:
            try:
                project = Project.objects.get(id=self.project_id)
            except Project.DoesNotExist:
                logger.info('Project `%s` does not exist anymore, stopping build',
                            self.project_name)
                return check_pulse, True

            if not project.notebook or not project.notebook.is_running:
                logger.info('Project `%s` does not have a notebook anymore, stopping build',
                            self.project_name)
                return check_pulse, True
            else:
                check_pulse = 0
        return check_pulse, False


def build_notebook_job(project, job):
    return build_job(project=project,
                     job=job,
                     job_builder=NotebookDockerBuilder,
                     image_tag=NotebookDockerBuilder.LATEST_IMAGE_TAG)
