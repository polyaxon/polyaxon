# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import shutil

import click

from polyaxon_deploy.operators.compose import ComposeOperator
from polyaxon_deploy.operators.docker import DockerOperator
from polyaxon_deploy.operators.helm import HelmOperator
from polyaxon_deploy.operators.kubectl import KubectlOperator
from polyaxon_deploy.schemas.deployment_types import DeploymentTypes

from polyaxon_cli.exceptions import PolyaxonDeploymentConfigError
from polyaxon_cli.managers.compose import ComposeConfigManager
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client.transport import Transport


class DeployManager(object):

    def __init__(self, config=None, filepath=None, manager_path=None, dry_run=False):
        self.config = config
        self.filepath = filepath
        self.manager_path = manager_path
        self.dry_run = dry_run
        self.kubectl = KubectlOperator()
        self.helm = HelmOperator()
        self.docker = DockerOperator()
        self.compose = ComposeOperator()

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
        if not self.kubectl.check():
            raise PolyaxonDeploymentConfigError('kubectl is required to run this command.')
        Printer.print_success('kubectl is installed')

        if not self.helm.check():
            raise PolyaxonDeploymentConfigError('helm is required to run this command.')
        Printer.print_success('helm is installed')

        # Check that polyaxon/polyaxon is set and up-to date
        self.helm.execute(args=['repo', 'add', 'polyaxon', 'https://charts.polyaxon.com'])
        self.helm.execute(args=['repo', 'update'])
        return True

    def check_for_docker_compose(self):
        # Deployment on docker compose requires Docker & Docker Compose to be installed
        if not self.docker.check():
            raise PolyaxonDeploymentConfigError('Docker is required to run this command.')
        Printer.print_success('Docker is installed')

        if not self.compose.check():
            raise PolyaxonDeploymentConfigError('Docker Compose is required to run this command.')
        Printer.print_success('Docker Compose is installed')

        # Check that .polyaxon/.compose is set and up-to date
        if ComposeConfigManager.is_initialized():
            Printer.print_success('Docker Compose deployment is initialised.')
        return True

    def check_for_docker(self):
        if not self.docker.check():
            raise PolyaxonDeploymentConfigError('Docker is required to run this command.')
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
        if self.dry_run:
            args += ['--debug', '--dry-run']

        click.echo('Running install command ...')
        stdout = self.helm.execute(args=args)
        click.echo(stdout)
        Printer.print_success('Deployment finished.')

    def install_on_docker_compose(self):
        path = ComposeConfigManager.get_config_file_path()
        path = '/'.join(path.split('/')[:-1])
        # Fetch docker-compose
        Transport().download(
            url='https://github.com/polyaxon/polyaxon-compose/archive/master.tar.gz',
            filename=path + '/file',
            untar=True,
            delete_tar=True,
            extract_path=path)
        # Move necessary info
        shutil.copy(path + '/polyaxon-compose-master/docker-compose.yml',
                    path + '/docker-compose.yml')
        shutil.copy(path + '/polyaxon-compose-master/components.env',
                    path + '/components.env')
        shutil.copy(path + '/polyaxon-compose-master/base.env',
                    path + '/base.env')
        shutil.rmtree(path + '/polyaxon-compose-master/')
        # Generate env from config
        ComposeConfigManager.set_config(self.compose.generate_env(self.config))
        Printer.print_success('Docker Compose deployment is initialised.')
        if self.dry_run:
            Printer.print_success('Polyaxon generated deployment env.')
            return
        self.docker.execute(['volume', 'create', '--name=polyaxon-postgres'])
        Printer.print_success('Docker volume created.')
        self.compose.execute(['-f', path + '/docker-compose.yml', 'up', '-d'])
        Printer.print_success('Deployment is running in the background.')
        Printer.print_success('You can configure your CLI by running: '
                              'polyaxon config set --host=localhost --port=8000.')

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
        if self.dry_run:
            args += ['--debug', '--dry-run']
        click.echo('Running upgrade command ...')
        stdout = self.helm.execute(args=args)
        click.echo(stdout)
        Printer.print_success('Deployment upgraded.')

    def upgrade_on_docker_compose(self):
        self.install_on_docker_compose()

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

    def teardown_on_docker_compose(self):
        path = ComposeConfigManager.get_config_file_path()
        path = '/'.join(path.split('/')[:-1])
        self.compose.execute(['-f', path + '/docker-compose.yml', 'down'])

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
            self.teardown_on_docker_compose()
        elif self.is_docker:
            self.teardown_on_docker(hooks=hooks)
        elif self.is_heroku:
            self.teardown_on_heroku(hooks=hooks)
