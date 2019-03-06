import conf

from scheduler.spawners.dockerizer_spawner import DockerizerSpawner
from scheduler.spawners.templates import constants


class KanikoSpawner(DockerizerSpawner):
    @staticmethod
    def get_job_docker_image(job_docker_image):
        return job_docker_image or conf.get('JOB_KANIKO_IMAGE')

    @staticmethod
    def get_job_docker_image_pull_policy(job_docker_image_pull_policy):
        return job_docker_image_pull_policy or conf.get('JOB_KANIKO_IMAGE_PULL_POLICY')

    def get_env_vars(self):
        return None

    def get_pod_command_args(self):
        args = ["-c", constants.BUILD_CONTEXT,
                "-d", "{}:{}".format(self.image_name, self.image_tag)]
        if self.in_cluster_registry:
            args.append("--insecure")
        return None, args
