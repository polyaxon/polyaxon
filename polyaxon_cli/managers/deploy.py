# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from polyaxon_deploy.operators.helm import HelmOperator
from polyaxon_deploy.operators.kubectl import KubectlOperator
from polyaxon_deploy.schemas.deployment_types import DeploymentTypes

from polyaxon_cli.exceptions import PolyaxonDeploymentConfigError
from polyaxon_cli.utils.formatting import Printer


class DeployManager(object):

    def __init__(self, config=None, filepath=None, manager_path=None):
        self.config = config
        self.filepath = filepath
        self.manager_path = manager_path
        self.kubectl = KubectlOperator()
        self.helm = HelmOperator()

    @property
    def deployment_type(self):
        if self.config and self.config.deploymentType:
            return self.config.deploymentType
        return DeploymentTypes.KUBERNETES

    @property
    def deployment_version(self):
        if self.config and self.config.deploymentVersion:
            return self.config.deploymentVersion
        return None

    @property
    def is_kubernetes(self):
        return self.deployment_type in {DeploymentTypes.KUBERNETES,
                                        DeploymentTypes.MINIKUBE,
                                        DeploymentTypes.MICRO_K8S}

    @property
    def is_docker_compose(self):
        return self.deployment_type == DeploymentTypes.DOCKER_COMPOSE

    @property
    def is_docker(self):
        return self.deployment_type == DeploymentTypes.DOCKER

    @property
    def is_heroku(self):
        return self.deployment_type == DeploymentTypes.HEROKU

    @property
    def is_valid(self):
        return self.deployment_type in DeploymentTypes.VALUES

    def check_for_kubernetes(self):
        # Deployment on k8s requires helm & kubectl to be installed
        command_exist = self.kubectl.execute(args=[], is_json=False)
        if not command_exist:
            raise PolyaxonDeploymentConfigError('kubectl is required to run this command.')
        Printer.print_success('kubectl is installed')

        command_exist = self.helm.execute(args=[])
        if not command_exist:
            raise PolyaxonDeploymentConfigError('helm is required to run this command.')
        Printer.print_success('helm is installed')

        # Check the version to ensure that there's a connection
        command_exist = self.kubectl.execute(args=['version'])
        if not command_exist:
            raise PolyaxonDeploymentConfigError('kubectl has no kubernetes config.')

        command_exist = self.helm.execute(args=['version'])
        if not command_exist:
            raise PolyaxonDeploymentConfigError(
                'helm is not configured or kubernetes config is not found.')

        # Check that polyaxon/polyaxon is set and up-to date
        self.helm.execute(args=['repo', 'add', 'polyaxon', 'https://charts.polyaxon.com'])
        self.helm.execute(args=['repo', 'update'])
        return True

    def check_for_docker_compose(self):
        return True

    def check_for_docker(self):
        return True

    def check_for_heroku(self):
        return True

    def nvidia_device_plugin(self):
        return 'https://github.com/NVIDIA/k8s-device-plugin/blob/v1.10/nvidia-device-plugin.yml'

    def check(self):
        """Add platform specific checks"""
        if not self.is_valid:
            raise PolyaxonDeploymentConfigError(
                'Deployment type `{}` not supported'.format(self.deployment_type))
        check = False
        if self.is_kubernetes:
            check = self.check_for_kubernetes()
        elif self.is_docker_compose:
            check = self.check_for_docker_compose()
        elif self.is_docker:
            check = self.check_for_docker()
        elif self.is_heroku:
            check = self.check_for_heroku()
        if not check:
            raise PolyaxonDeploymentConfigError(
                'Deployment `{}` is not valid'.format(self.deployment_type))

    def install_on_kubernetes(self):
        args = ['install']
        if self.manager_path:
            args += [self.manager_path]
        else:
            args += ['polyaxon/polyaxon']

        args += ['--name=polyaxon', '--namespace=polyaxon']
        if self.filepath:
            args += ['-f', self.filepath]
        if self.deployment_version:
            args += ['--version', self.deployment_version]

        click.echo('Running install command ...')
        stdout = self.helm.execute(args=args)
        click.echo(stdout)
        Printer.print_success('Deployment finished.')

    def install_on_docker_compose(self):
        pass

    def install_on_docker(self):
        pass

    def install_on_heroku(self):
        pass

    def install(self):
        """Install polyaxon using the current config to the correct platform."""
        if not self.is_valid:
            raise PolyaxonDeploymentConfigError(
                'Deployment type `{}` not supported'.format(self.deployment_type))

        if self.is_kubernetes:
            self.install_on_kubernetes()
        elif self.is_docker_compose:
            self.install_on_docker_compose()
        elif self.is_docker:
            self.install_on_docker()
        elif self.is_heroku:
            self.install_on_heroku()

    def upgrade_on_kubernetes(self):
        args = ['upgrade', 'polyaxon']
        if self.manager_path:
            args += [self.manager_path]
        else:
            args += ['polyaxon/polyaxon']
        if self.filepath:
            args += ['-f', self.filepath]
        if self.deployment_version:
            args += ['--version', self.deployment_version]
        click.echo('Running upgrade command ...')
        stdout = self.helm.execute(args=args)
        click.echo(stdout)
        Printer.print_success('Deployment upgraded.')

    def upgrade_on_docker_compose(self):
        pass

    def upgrade_on_docker(self):
        pass

    def upgrade_on_heroku(self):
        pass

    def upgrade(self):
        """Upgrade deployment."""
        if not self.is_valid:
            raise PolyaxonDeploymentConfigError(
                'Deployment type `{}` not supported'.format(self.deployment_type))

        if self.is_kubernetes:
            self.upgrade_on_kubernetes()
        elif self.is_docker_compose:
            self.upgrade_on_docker_compose()
        elif self.is_docker:
            self.upgrade_on_docker()
        elif self.is_heroku:
            self.upgrade_on_heroku()

    def teardown_on_kubernetes(self, hooks):
        args = ['delete', '--purge', 'polyaxon']
        if not hooks:
            args += ['--no-hooks']
        click.echo('Running teardown command ...')
        self.helm.execute(args=args)
        Printer.print_success('Deployment successfully deleted.')

    def teardown_on_docker_compose(self, hooks):
        pass

    def teardown_on_docker(self, hooks):
        pass

    def teardown_on_heroku(self, hooks):
        pass

    def teardown(self, hooks=True):
        """Teardown Polyaxon."""
        if not self.is_valid:
            raise PolyaxonDeploymentConfigError(
                'Deployment type `{}` not supported'.format(self.deployment_type))

        if self.is_kubernetes:
            self.teardown_on_kubernetes(hooks=hooks)
        elif self.is_docker_compose:
            self.teardown_on_docker_compose(hooks=hooks)
        elif self.is_docker:
            self.teardown_on_docker(hooks=hooks)
        elif self.is_heroku:
            self.teardown_on_heroku(hooks=hooks)
