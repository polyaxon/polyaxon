def get_experiment_group_subpath(experiment_group_name: str) -> str:
    values = experiment_group_name.split('.')
    values.insert(2, 'groups')
    return '/'.join(values)
