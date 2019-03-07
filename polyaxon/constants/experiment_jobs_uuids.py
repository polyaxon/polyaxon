import uuid


def get_experiment_job_uuid(experiment_uuid, task_type, task_index):
    if isinstance(experiment_uuid, str):
        experiment_uuid = uuid.UUID(experiment_uuid)
    return uuid.uuid5(experiment_uuid, '{}-{}'.format(task_type, task_index)).hex
