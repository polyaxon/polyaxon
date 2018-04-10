from polyaxon.utils import config

PROJECT_APPS = (
    'polyaxon',
    'libs.apps.LibsConfig',
    'users.apps.UsersConfig',
    'clusters.apps.ClustersConfig',
    'pipelines.apps.PipelinesConfig',
    'jobs.apps.JobsConfig',
    'plugins.apps.PluginsConfig',
    'projects.apps.ProjectsConfig',
    'experiment_groups.apps.ExperimentGroupsConfig',
    'experiments.apps.ExperimentsConfig',
    'repos.apps.ReposConfig',
    'versions.apps.VersionsConfig',
    'events.apps.EventsConfig',
)

DEPLOY_RUNNER = config.get_boolean('POLYAXON_DEPLOY_RUNNER', is_optional=True) or True
if DEPLOY_RUNNER:
    PROJECT_APPS += ('runner.apps.RunnerConfig',)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

INSTALLED_APPS += THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
