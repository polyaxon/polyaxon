# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from polyaxon_deploy.operators.cmd_operator import CmdOperator


class ComposeOperator(CmdOperator):
    CMD = 'docker-compose'

    @classmethod
    def params(cls, args):
        params = [cls.CMD] + args
        return params

    @classmethod
    def check(cls):
        command_exist = cls.execute(args=['version'])
        if not command_exist:
            return False
        return True

    @classmethod
    def execute(cls, args, stream=False):
        params = cls.params(args)
        return cls._execute(params=params, env=None, stream=stream)

    @classmethod
    def generate_env(cls, config):
        # pylint:disable=too-many-statements
        # pylint:disable=too-many-branches
        template = '{}={}'
        env = [
            template.format('POLYAXON_DEPLOYMENT_TYPE', config.deploymentType),
        ]
        if config.deploymentType:
            env.append(template.format('POLYAXON_CHART_VERSION', config.deploymentType))
        if config.clusterId:
            env.append(template.format('POLYAXON_CLUSTER_ID', config.clusterId))
        if config.namespace:
            env.append(template.format('POLYAXON_K8S_NAMESPACE', config.namespace))
        env.append(template.format('POLYAXON_SECRET_KEY',
                                   config.polyaxonSecret or uuid.uuid4().hex))
        env.append(template.format('POLYAXON_SECRET_INTERNAL_TOKEN',
                                   config.internalToken or uuid.uuid4().hex))
        if config.ssl and config.ssl.enabled and config.ssl.path:
            env.append(template.format('POLYAXON_SSL_ENABLED', config.ssl.enabled))
            env.append(template.format('POLYAXON_SSL_PATH', config.ssl.path))
        env.append(template.format('POLYAXON_ADMIN_VIEW_ENABLED', config.adminViewEnabled or False))
        if config.adminModels:
            env.append(template.format('POLYAXON_ADMIN_MODELS', config.adminModels))
        if config.timeZone:
            env.append(
                template.format('POLYAXON_TIMEZONE', config.timeZone or False))
        if config.worker and config.worker.concurrency:
            env.append(
                template.format('POLYAXON_WORKER_CONCURRENCY', config.worker.concurrency or 2))
        else:
            env.append(
                template.format('POLYAXON_WORKER_CONCURRENCY', config.worker.concurrency or 2))
        if config.email:
            env.append(template.format('POLYAXON_EMAIL_HOST', config.email.host))
            env.append(template.format('POLYAXON_EMAIL_PORT', config.email.port))
            env.append(template.format('POLYAXON_EMAIL_USE_TLS', config.email.useTls))
            if config.email.hostUser:
                env.append(template.format('POLYAXON_EMAIL_HOST_USER', config.email.hostUser))
            if config.email.backend:
                env.append(template.format('POLYAXON_EMAIL_BACKEND', config.email.backend))

        if config.hostName:
            env.append(template.format('POLYAXON_API_HOST', config.hostName))
        if config.allowedHosts:
            env.append(template.format('POLYAXON_ALLOWED_HOSTS', config.allowedHosts))

        if config.intervals:
            env.append(template.format('POLYAXON_INTERVALS_EXPERIMENTS_SCHEDULER',
                                       config.intervals.experimentsScheduler))
            env.append(template.format('POLYAXON_INTERVALS_EXPERIMENTS_SYNC',
                                       config.intervals.experimentsSync))
            env.append(template.format('POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_INFO',
                                       config.intervals.clustersUpdateSystemInfo))
            env.append(template.format('POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_NODES',
                                       config.intervals.clustersUpdateSystemNodes))
            env.append(template.format('POLYAXON_INTERVALS_PIPELINES_SCHEDULER',
                                       config.intervals.pipelinesScheduler))
            env.append(template.format('POLYAXON_INTERVALS_OPERATIONS_DEFAULT_RETRY_DELAY',
                                       config.intervals.operationsDefaultRetryDelay))
            env.append(template.format('POLYAXON_INTERVALS_OPERATIONS_MAX_RETRY_DELAY',
                                       config.intervals.operationsMaxRetryDelay))

        if config.logLevel:
            env.append(template.format('POLYAXON_LOG_LEVEL', config.logLevel))
        if config.trackerBackend:
            env.append(template.format('POLYAXON_TRACKER_BACKEND', config.trackerBackend))
        if config.securityContext:
            env.append(template.format('POLYAXON_SECURITY_CONTEXT_USER',
                                       config.securityContext.user))
            env.append(template.format('POLYAXON_SECURITY_CONTEXT_GROUP',
                                       config.securityContext.groups))
        if config.postgresql and not config.postgresql.enabled:
            env.append(template.format('POLYAXON_DB_USER',
                                       config.externalServices.postgresql.user))
            env.append(template.format('POLYAXON_DB_PASSWORD',
                                       config.externalServices.postgresql.password))
            env.append(template.format('POLYAXON_DB_NAME',
                                       config.externalServices.postgresql.database))
            env.append(template.format('POLYAXON_DB_HOST',
                                       config.externalServices.postgresql.host))

        return '\n'.join(env)
