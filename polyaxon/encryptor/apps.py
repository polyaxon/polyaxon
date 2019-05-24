from django.apps import AppConfig


class EncryptorConfig(AppConfig):
    name = 'encryptor'
    verbose_name = 'encryptor'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_encryptor_service()
