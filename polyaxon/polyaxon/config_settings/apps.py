# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

PROJECT_APPS = (
    'polyaxon',
    'libs.apps.LibsConfig',
    'users.apps.UsersConfig',
    'clusters.apps.ClustersConfig',
    'jobs.apps.JobsConfig',
    'plugins.apps.PluginsConfig',
    'projects.apps.ProjectsConfig',
    'experiments.apps.ExperimentsConfig',
    'repos.apps.ReposConfig',
    'dockerizer.apps.DockerizerConfig',
    'versions.apps.VersionsConfig',
    'events.apps.EventsConfig',
    'spawner.apps.SpawnerConfig',
    'schedulers.apps.SchedulersConfig',
)

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

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
