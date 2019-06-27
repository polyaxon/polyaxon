from django.contrib.admin import site

from administration.register import (
    activitylogs,
    artifacts_stores,
    bookmarks,
    build_jobs,
    clusters,
    config_maps,
    config_options,
    data_stores,
    experiment_groups,
    experiments,
    groups,
    job_resources,
    jobs,
    logs_stores,
    nodes,
    notebooks,
    notifications,
    owners,
    pipelines,
    projects,
    repos,
    searches,
    secrets,
    sso,
    tensorboards,
    tokens,
    users,
    versions
)

REGISTRY = {
    'artifacts_stores': artifacts_stores,
    'activitylogs': activitylogs,
    'bookmarks': bookmarks,
    'build_jobs': build_jobs,
    'clusters': clusters,
    'config_maps': config_maps,
    'config_options': config_options,
    'data_stores': data_stores,
    'experiment_groups': experiment_groups,
    'experiments': experiments,
    'job_resources': job_resources,
    'jobs': jobs,
    'logs_stores': logs_stores,
    'nodes': nodes,
    'notebooks': notebooks,
    'notifications': notifications,
    'owners': owners,
    'pipelines': pipelines,
    'repos': repos,
    'searches': searches,
    'secrets': secrets,
    'sso': sso,
    'tensorboards': tensorboards,
    'versions': versions,
}


def register(models=None):
    admin_register = site.register
    groups.register(admin_register)
    tokens.register(admin_register)
    users.register(admin_register)
    projects.register(admin_register)

    if not models:
        return

    for model in models:
        if model in REGISTRY:
            REGISTRY[model].register(admin_register)
