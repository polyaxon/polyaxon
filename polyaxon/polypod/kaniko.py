import conf

from options.registry.build_jobs import KANIKO_DOCKER_IMAGE, KANIKO_IMAGE_PULL_POLICY
from polypod.dockerizer import DockerizerSpawner
from polypod.templates import constants


class KanikoSpawner(DockerizerSpawner):
    SECRET_MOUNT_PATH = '/kaniko/.docker'  # noqa

    @staticmethod
    def get_job_docker_image(job_docker_image):
        return job_docker_image or conf.get(KANIKO_DOCKER_IMAGE)

    @staticmethod
    def get_job_docker_image_pull_policy(job_docker_image_pull_policy):
        return job_docker_image_pull_policy or conf.get(KANIKO_IMAGE_PULL_POLICY)

    def get_env_vars(self):
        return None

    def get_pod_command_args(self, image_name, image_tag, nocache, insecure):
        args = ["-c", constants.BUILD_CONTEXT,
                "-d", "{}:{}".format(image_name, image_tag)]
        if insecure:
            args.append("--insecure")
        return None, args
