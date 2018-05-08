from polyaxon.utils import config

PROJECT_APPS = (
    'polyaxon',
    'libs.apps.LibsConfig',
    'users.apps.UsersConfig',
    'versions.apps.VersionsConfig',
    'clusters.apps.ClustersConfig',
    'projects.apps.ProjectsConfig',
    'repos.apps.ReposConfig',
    'jobs.apps.JobsConfig',
    'experiment_groups.apps.ExperimentGroupsConfig',
    'experiments.apps.ExperimentsConfig',
    'pipelines.apps.PipelinesConfig',
    'event_monitors.apps.EventMonitorsConfig',
)

DEPLOY_RUNNER = config.get_boolean('POLYAXON_DEPLOY_RUNNER', is_optional=True, default=True)
if DEPLOY_RUNNER:
    PROJECT_APPS += (
        'plugins.apps.PluginsConfig',
        'runner.apps.RunnerConfig',
        'runner.nodes.apps.NodesConfig',
    )

THIRD_PARTY_APPS = (
    'raven.contrib.django.raven_compat',
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
