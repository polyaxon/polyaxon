from options import option_namespaces, option_subjects
from options.option import Option, OptionStores
from options.types import CONF_TYPES

DOWNLOADS_ROOT_ARTIFACTS = '{}_{}'.format(option_namespaces.DOWNLOADS_ROOT,
                                          option_subjects.ARTIFACTS)
DOWNLOADS_ROOT_LOGS = '{}_{}'.format(option_namespaces.DOWNLOADS_ROOT,
                                     option_subjects.LOGS)


class DownloadRootOption(Option):
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class DownloadRootArtifacts(DownloadRootOption):
    key = DOWNLOADS_ROOT_ARTIFACTS
    description = 'Downloads root path for artifacts'


class DownloadRootLogs(DownloadRootOption):
    key = DOWNLOADS_ROOT_LOGS
    description = 'Downloads root path for logs'
