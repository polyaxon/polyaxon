def get_labels(app, project_name, project_uuid, job_name, job_uuid, role=None, type=None):
    # pylint:disable=redefined-builtin
    labels = {'app': app,
              'project_name': project_name,
              'project_uuid': project_uuid,
              'job_name': job_name,
              'job_uuid': job_uuid}
    if role:
        labels['role'] = role
    if type:
        labels['type'] = type
    return labels
