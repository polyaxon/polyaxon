from django.apps import AppConfig


class CompilerConfig(AppConfig):
    name = 'compiler'
    verbose_name = 'Compiler'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_compiler_service()
