def get_user_url(username):
    return '/{}'.format(username)


def get_project_url(unique_name):
    values = unique_name.split('.')
    return '{}/{}'.format(get_user_url(values[0]), values[1])


def get_user_project_url(username, project_name):
    return '{}/{}'.format(get_user_url(username), project_name)


def get_experiment_url(unique_name):
    values = unique_name.split('.')
    project_url = get_user_project_url(username=values[0], project_name=values[1])
    return '{}/experiments/{}'.format(project_url, values[2] if len(values) == 3 else values[3])


def get_experiment_group_url(unique_name):
    values = unique_name.split('.')
    project_url = get_user_project_url(username=values[0], project_name=values[1])
    return '{}/groups/{}'.format(project_url, values[2])


def get_job_url(unique_name):
    values = unique_name.split('.')
    project_url = get_user_project_url(username=values[0], project_name=values[1])
    return '{}/jobs/{}'.format(project_url, values[2])


def get_build_url(unique_name):
    values = unique_name.split('.')
    project_url = get_user_project_url(username=values[0], project_name=values[1])
    return '{}/builds/{}'.format(project_url, values[2])
