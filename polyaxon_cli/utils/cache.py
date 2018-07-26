from polyaxon_cli.managers.project import ProjectManager


def cache(config_manager, response):
    # Set caching only if we have an initialized project
    if ProjectManager.is_initialized():
        config_manager.set_config(response)
