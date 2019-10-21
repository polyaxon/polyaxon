from options import option_namespaces, option_subjects
from options.option import Option, OptionStores
from options.types import CONF_TYPES

ARCHIVES_ROOT_REPOS = '{}_{}'.format(option_namespaces.ARCHIVES_ROOT,
                                     option_subjects.REPOS)
ARCHIVES_ROOT_ARTIFACTS = '{}_{}'.format(option_namespaces.ARCHIVES_ROOT,
                                         option_subjects.ARTIFACTS)
ARCHIVES_ROOT_LOGS = '{}_{}'.format(option_namespaces.ARCHIVES_ROOT,
                                    option_subjects.LOGS)


class ArchivesOption(Option):
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class ArchivesRootRepos(ArchivesOption):
    key = ARCHIVES_ROOT_REPOS
    description = 'Archive root path for repos'


class ArchivesRootArtifacts(ArchivesOption):
    key = ARCHIVES_ROOT_ARTIFACTS
    description = 'Archive root path for artifacts'


class ArchivesRootLogs(ArchivesOption):
    key = ARCHIVES_ROOT_LOGS
    description = 'Archive root path for logs'
