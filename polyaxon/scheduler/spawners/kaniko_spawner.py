from scheduler.spawners.dockerizer_spawner import DockerizerSpawner
from scheduler.spawners.templates import constants


class KanikoSpawner(DockerizerSpawner):

    def get_env_vars(self):
        return None

    def get_pod_command_args(self):
        return None, ["-c", constants.BUILD_CONTEXT,
                      "-d", "{}:{}".format(self.image_name, self.image_tag),
                      "--insecure"]
