from polyaxon.config_manager import config

# Labels
APP_LABELS_TENSORBOARD = config.get_string('POLYAXON_APP_LABELS_TENSORBOARD',
                                           is_optional=True,
                                           default='polyaxon-tensorboard')
APP_LABELS_NOTEBOOK = config.get_string('POLYAXON_APP_LABELS_NOTEBOOK',
                                        is_optional=True,
                                        default='polyaxon-notebook')
APP_LABELS_DOCKERIZER = config.get_string('POLYAXON_APP_LABELS_DOCKERIZER',
                                          is_optional=True,
                                          default='polyaxon-dockerizer')
APP_LABELS_EXPERIMENT = config.get_string('POLYAXON_APP_LABELS_EXPERIMENT',
                                          is_optional=True,
                                          default='polyaxon-experiment')
APP_LABELS_JOB = config.get_string('POLYAXON_APP_LABELS_JOB',
                                   is_optional=True,
                                   default='polyaxon-job')
