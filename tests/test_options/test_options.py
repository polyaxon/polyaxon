import pytest

from options.registry import (
    affinities,
    auth_azure,
    auth_bitbucket,
    auth_github,
    auth_gitlab,
    build_jobs,
    core,
    env_vars,
    k8s_config_maps,
    k8s_secrets,
    node_selectors,
    notebooks,
    scheduler,
    tensorboards,
    tolerations
)
from tests.base.case import BaseTest


@pytest.mark.options_mark
class TestOptions(BaseTest):
    def test_options_core(self):
        assert core.PasswordLength.get_key_subject() == 'PASSWORD_LENGTH'
        assert core.PasswordLength.get_namespace() is None
        assert core.AdminViewEnabled.default is True
        assert core.AdminViewEnabled.is_global is True
        assert core.AdminViewEnabled.is_optional is True
        assert core.AdminViewEnabled.get_key_subject() == 'ADMIN_VIEW_ENABLED'
        assert core.AdminViewEnabled.get_namespace() is None
        assert core.AdminViewEnabled.default is True
        assert core.AdminViewEnabled.is_global is True
        assert core.AdminViewEnabled.is_optional is True
        assert core.Logging.get_key_subject() == 'LOGGING'
        assert core.Logging.get_namespace() is None

    def test_options_affinities(self):
        assert affinities.AffinitiesBuildJobs.get_key_subject() == 'BUILD_JOBS'
        assert affinities.AffinitiesJobs.get_key_subject() == 'JOBS'
        assert affinities.AffinitiesExperiments.get_key_subject() == 'EXPERIMENTS'
        assert affinities.AffinitiesNotebooks.get_key_subject() == 'NOTEBOOKS'
        assert affinities.AffinitiesTensorboards.get_key_subject() == 'TENSORBOARDS'
        assert affinities.AffinitiesBuildJobs.get_namespace() == 'AFFINITIES'
        assert affinities.AffinitiesJobs.get_namespace() == 'AFFINITIES'
        assert affinities.AffinitiesExperiments.get_namespace() == 'AFFINITIES'
        assert affinities.AffinitiesNotebooks.get_namespace() == 'AFFINITIES'
        assert affinities.AffinitiesTensorboards.get_namespace() == 'AFFINITIES'

    def test_options_auth_azure(self):
        assert auth_azure.AuthAzureEnabled.get_key_subject() == 'ENABLED'
        assert auth_azure.AuthAzureVerificationSchedule.get_key_subject() == 'VERIFICATION_SCHEDULE'
        assert auth_azure.AuthAzureTenantId.get_key_subject() == 'TENANT_ID'
        assert auth_azure.AuthAzureClientId.get_key_subject() == 'CLIENT_ID'
        assert auth_azure.AuthAzureClientSecret.get_key_subject() == 'CLIENT_SECRET'
        assert auth_azure.AuthAzureEnabled.get_namespace() == 'AUTH_AZURE'
        assert auth_azure.AuthAzureVerificationSchedule.get_namespace() == 'AUTH_AZURE'
        assert auth_azure.AuthAzureTenantId.get_namespace() == 'AUTH_AZURE'
        assert auth_azure.AuthAzureClientId.get_namespace() == 'AUTH_AZURE'
        assert auth_azure.AuthAzureClientSecret.get_namespace() == 'AUTH_AZURE'

    def test_options_auth_bitbucket(self):
        assert auth_bitbucket.AuthBitbucketEnabled.get_key_subject() == 'ENABLED'
        assert (auth_bitbucket.AuthBitbucketVerificationSchedule.get_key_subject() ==
                'VERIFICATION_SCHEDULE')
        assert auth_bitbucket.AuthBitbucketClientId.get_key_subject() == 'CLIENT_ID'
        assert auth_bitbucket.AuthBitbucketClientSecret.get_key_subject() == 'CLIENT_SECRET'
        assert auth_bitbucket.AuthBitbucketEnabled.get_namespace() == 'AUTH_BITBUCKET'
        assert auth_bitbucket.AuthBitbucketVerificationSchedule.get_namespace() == 'AUTH_BITBUCKET'
        assert auth_bitbucket.AuthBitbucketClientId.get_namespace() == 'AUTH_BITBUCKET'
        assert auth_bitbucket.AuthBitbucketClientSecret.get_namespace() == 'AUTH_BITBUCKET'

    def test_options_auth_github(self):
        assert auth_github.AuthGithubEnabled.get_key_subject() == 'ENABLED'
        assert (auth_github.AuthGithubVerificationSchedule.get_key_subject() ==
                'VERIFICATION_SCHEDULE')
        assert auth_github.AuthGithubClientId.get_key_subject() == 'CLIENT_ID'
        assert auth_github.AuthGithubClientSecret.get_key_subject() == 'CLIENT_SECRET'
        assert auth_github.AuthGithubEnabled.get_namespace() == 'AUTH_GITHUB'
        assert auth_github.AuthGithubVerificationSchedule.get_namespace() == 'AUTH_GITHUB'
        assert auth_github.AuthGithubClientId.get_namespace() == 'AUTH_GITHUB'
        assert auth_github.AuthGithubClientSecret.get_namespace() == 'AUTH_GITHUB'

    def test_options_auth_gitlab(self):
        assert auth_gitlab.AuthGitlabEnabled.get_key_subject() == 'ENABLED'
        assert (auth_gitlab.AuthGitlabVerificationSchedule.get_key_subject() ==
                'VERIFICATION_SCHEDULE')
        assert auth_gitlab.AuthGitlabUrl.get_key_subject() == 'URL'
        assert auth_gitlab.AuthGitlabClientId.get_key_subject() == 'CLIENT_ID'
        assert auth_gitlab.AuthGitlabClientSecret.get_key_subject() == 'CLIENT_SECRET'
        assert auth_gitlab.AuthGitlabEnabled.get_namespace() == 'AUTH_GITLAB'
        assert auth_gitlab.AuthGitlabVerificationSchedule.get_namespace() == 'AUTH_GITLAB'
        assert auth_gitlab.AuthGitlabUrl.get_namespace() == 'AUTH_GITLAB'
        assert auth_gitlab.AuthGitlabClientId.get_namespace() == 'AUTH_GITLAB'
        assert auth_gitlab.AuthGitlabClientSecret.get_namespace() == 'AUTH_GITLAB'

    def test_options_build_jobs(self):
        assert build_jobs.BuildJobsBackend.get_key_subject() == 'BACKEND'
        assert build_jobs.BuildJobsLangEnv.get_key_subject() == 'LANG_ENV'
        assert build_jobs.BuildJobsImagePullPolicy.get_key_subject() == 'IMAGE_PULL_POLICY'
        assert build_jobs.KanikoDockerImage.get_key_subject() == 'DOCKER_IMAGE'
        assert build_jobs.KanikoImagePullPolicy.get_key_subject() == 'IMAGE_PULL_POLICY'
        assert build_jobs.BuildJobsBackend.get_namespace() == 'BUILD_JOBS'
        assert build_jobs.BuildJobsLangEnv.get_namespace() == 'BUILD_JOBS'
        assert build_jobs.BuildJobsImagePullPolicy.get_namespace() == 'BUILD_JOBS'
        assert build_jobs.KanikoDockerImage.get_namespace() == 'KANIKO'
        assert build_jobs.KanikoImagePullPolicy.get_namespace() == 'KANIKO'

    def test_options_env_vars(self):
        assert env_vars.EnvVarsBuildJobs.get_key_subject() == 'BUILD_JOBS'
        assert env_vars.EnvVarsJobs.get_key_subject() == 'JOBS'
        assert env_vars.EnvVarsExperiments.get_key_subject() == 'EXPERIMENTS'
        assert env_vars.EnvVarsNotebooks.get_key_subject() == 'NOTEBOOKS'
        assert env_vars.EnvVarsTensorboards.get_key_subject() == 'TENSORBOARDS'
        assert env_vars.EnvVarsBuildJobs.get_namespace() == 'ENV_VARS'
        assert env_vars.EnvVarsJobs.get_namespace() == 'ENV_VARS'
        assert env_vars.EnvVarsExperiments.get_namespace() == 'ENV_VARS'
        assert env_vars.EnvVarsNotebooks.get_namespace() == 'ENV_VARS'
        assert env_vars.EnvVarsTensorboards.get_namespace() == 'ENV_VARS'

    def test_options_k8s_config_maps(self):
        assert k8s_config_maps.K8SConfigMapsBuildJobs.get_key_subject() == 'BUILD_JOBS'
        assert k8s_config_maps.K8SConfigMapsJobs.get_key_subject() == 'JOBS'
        assert k8s_config_maps.K8SConfigMapsExperiments.get_key_subject() == 'EXPERIMENTS'
        assert k8s_config_maps.K8SConfigMapsNotebooks.get_key_subject() == 'NOTEBOOKS'
        assert k8s_config_maps.K8SConfigMapsTensorboards.get_key_subject() == 'TENSORBOARDS'
        assert k8s_config_maps.K8SConfigMapsBuildJobs.get_namespace() == 'K8S_CONFIG_MAPS'
        assert k8s_config_maps.K8SConfigMapsJobs.get_namespace() == 'K8S_CONFIG_MAPS'
        assert k8s_config_maps.K8SConfigMapsExperiments.get_namespace() == 'K8S_CONFIG_MAPS'
        assert k8s_config_maps.K8SConfigMapsNotebooks.get_namespace() == 'K8S_CONFIG_MAPS'
        assert k8s_config_maps.K8SConfigMapsTensorboards.get_namespace() == 'K8S_CONFIG_MAPS'

    def test_options_k8s_secrets(self):
        assert k8s_secrets.K8SSecretsBuildJobs.get_key_subject() == 'BUILD_JOBS'
        assert k8s_secrets.K8SSecretsJobs.get_key_subject() == 'JOBS'
        assert k8s_secrets.K8SSecretsExperiments.get_key_subject() == 'EXPERIMENTS'
        assert k8s_secrets.K8SSecretsNotebooks.get_key_subject() == 'NOTEBOOKS'
        assert k8s_secrets.K8SSecretsTensorboards.get_key_subject() == 'TENSORBOARDS'
        assert k8s_secrets.K8SSecretsBuildJobs.get_namespace() == 'K8S_SECRETS'
        assert k8s_secrets.K8SSecretsJobs.get_namespace() == 'K8S_SECRETS'
        assert k8s_secrets.K8SSecretsExperiments.get_namespace() == 'K8S_SECRETS'
        assert k8s_secrets.K8SSecretsNotebooks.get_namespace() == 'K8S_SECRETS'
        assert k8s_secrets.K8SSecretsTensorboards.get_namespace() == 'K8S_SECRETS'

    def test_options_node_selectors(self):
        assert node_selectors.NodeSelectorsBuildJobs.get_key_subject() == 'BUILD_JOBS'
        assert node_selectors.NodeSelectorsJobs.get_key_subject() == 'JOBS'
        assert node_selectors.NodeSelectorsExperiments.get_key_subject() == 'EXPERIMENTS'
        assert node_selectors.NodeSelectorsNotebooks.get_key_subject() == 'NOTEBOOKS'
        assert node_selectors.NodeSelectorsTensorboards.get_key_subject() == 'TENSORBOARDS'
        assert node_selectors.NodeSelectorsBuildJobs.get_namespace() == 'NODE_SELECTORS'
        assert node_selectors.NodeSelectorsJobs.get_namespace() == 'NODE_SELECTORS'
        assert node_selectors.NodeSelectorsExperiments.get_namespace() == 'NODE_SELECTORS'
        assert node_selectors.NodeSelectorsNotebooks.get_namespace() == 'NODE_SELECTORS'
        assert node_selectors.NodeSelectorsTensorboards.get_namespace() == 'NODE_SELECTORS'

    def test_options_notebooks(self):
        assert notebooks.NotebooksDockerImage.get_namespace() == 'NOTEBOOKS'
        assert notebooks.NotebooksBackend.get_namespace() == 'NOTEBOOKS'
        assert notebooks.NotebooksDockerImage.get_key_subject() == 'DOCKER_IMAGE'
        assert notebooks.NotebooksBackend.get_key_subject() == 'BACKEND'

    def test_options_tensorboards(self):
        assert tensorboards.TensorboardsDockerImage.get_namespace() == 'TENSORBOARDS'
        assert tensorboards.TensorboardsDockerImage.get_key_subject() == 'DOCKER_IMAGE'

    def test_options_tolerations(self):
        assert tolerations.TolerationsBuildJobs.get_namespace() == 'TOLERATIONS'
        assert tolerations.TolerationsJobs.get_namespace() == 'TOLERATIONS'
        assert tolerations.TolerationsExperiments.get_namespace() == 'TOLERATIONS'
        assert tolerations.TolerationsNotebooks.get_namespace() == 'TOLERATIONS'
        assert tolerations.TolerationsTensorboards.get_namespace() == 'TOLERATIONS'
        assert tolerations.TolerationsBuildJobs.get_key_subject() == 'BUILD_JOBS'
        assert tolerations.TolerationsJobs.get_key_subject() == 'JOBS'
        assert tolerations.TolerationsExperiments.get_key_subject() == 'EXPERIMENTS'
        assert tolerations.TolerationsNotebooks.get_key_subject() == 'NOTEBOOKS'
        assert tolerations.TolerationsTensorboards.get_key_subject() == 'TENSORBOARDS'

    def test_options_scheduler(self):
        assert scheduler.SchedulerCountdown.get_namespace() == 'SCHEDULER'
        assert scheduler.SchedulerCountdown.get_key_subject() == 'GLOBAL_COUNTDOWN'
