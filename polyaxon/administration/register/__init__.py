from django.contrib.admin import site

from administration.register import (
    activitylogs,
    bookmarks,
    build_jobs,
    clusters,
    experiment_groups,
    experiments,
    groups,
    job_resources,
    jobs,
    nodes,
    notebooks,
    notifications,
    owners,
    pipelines,
    projects,
    repos,
    searches,
    sso,
    tensorboards,
    tokens,
    users,
    versions
)


def register(models=None):
    admin_register = site.register
    groups.register(admin_register)
    if not models:
        tokens.register(admin_register)
        users.register(admin_register)
        return

    if 'activitylogs' in models:
        activitylogs.register(admin_register)
    if 'bookmarks' in models:
        bookmarks.register(admin_register)
    if 'build_jobs' in models:
        build_jobs.register(admin_register)
    if 'clusters' in models:
        clusters.register(admin_register)
    if 'experiment_groups' in models:
        experiment_groups.register(admin_register)
    if 'experiments' in models:
        experiments.register(admin_register)
    if 'job_resources' in models:
        job_resources.register(admin_register)
    if 'jobs' in models:
        jobs.register(admin_register)
    if 'nodes' in models:
        nodes.register(admin_register)
    if 'notebooks' in models:
        notebooks.register(admin_register)
    if 'notifications' in models:
        notifications.register(admin_register)
    if 'owners' in models:
        owners.register(admin_register)
    if 'pipelines' in models:
        pipelines.register(admin_register)
    if 'projects' in models:
        projects.register(admin_register)
    if 'repos' in models:
        repos.register(admin_register)
    if 'searches' in models:
        searches.register(admin_register)
    if 'sso' in models:
        sso.register(admin_register)
    if 'tensorboards' in models:
        tensorboards.register(admin_register)
    if 'versions' in models:
        versions.register(admin_register)
