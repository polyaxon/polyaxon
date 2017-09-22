from tensorflow.python.estimator import run_config

from polyaxon_schemas import settings


class RunConfig(run_config.RunConfig):
    CONFIG = settings.RunConfig

    @classmethod
    def from_config(cls, config):
        if not isinstance(config, cls.CONFIG):
            config = cls.CONFIG.from_dict(config)

        params = config.to_dict()
        return cls(**params)
