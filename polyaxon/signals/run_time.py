from django.utils.timezone import now

from constants.jobs import JobLifeCycle


def set_started_at(instance, status, starting_statuses, running_status=None):
    # We allow to override started_at if the value is running
    if instance.started_at is not None and status != running_status:
        return

    if status in starting_statuses:
        instance.started_at = now()


def set_finished_at(instance, status, is_done):
    if is_done(status) and instance.finished_at is None:
        instance.finished_at = now()
        if instance.started_at is None:
            instance.started_at = instance.created_at


def set_job_started_at(instance, status):
    set_started_at(
        instance=instance,
        status=status,
        starting_statuses=[JobLifeCycle.BUILDING, JobLifeCycle.SCHEDULED, JobLifeCycle.RUNNING],
        running_status=JobLifeCycle.RUNNING)


def set_job_finished_at(instance, status):
    set_finished_at(instance=instance, status=status, is_done=JobLifeCycle.is_done)
