from django.conf import settings


def get_sidecar_args(pod_id):
    return [pod_id,
            "--log_sleep_interval={}".format(settings.JOB_SIDECAR_LOG_SLEEP_INTERVAL),
            "--persist=true"]


def get_sidecar_command(app_label):
    if app_label == settings.APP_LABELS_JOB:
        return ["python3", "polyaxon/manage.py", "start_job_sidecar"]
    if app_label == settings.APP_LABELS_EXPERIMENT:
        return ["python3", "polyaxon/manage.py", "start_experiment_sidecar"]
