from libs.services import Service

from amqp import AMQPError
from redis import RedisError

from django.conf import settings

from polyaxon.settings import RoutingKeys, RunnerCeleryTasks
from libs.redis_db import RedisToStream
from polyaxon.celery_api import app as celery_app


class PublisherService(Service):
    __all__ = ('publish_experiment_log', 'setup')

    def __init__(self):
        self._logger = None

    def publish_experiment_log(self,
                               log_line,
                               status,
                               experiment_uuid,
                               experiment_name,
                               job_uuid,
                               task_type=None,
                               task_idx=None):
        try:
            log_line = log_line.decode('utf-8')
        except AttributeError:
            pass

        self._logger.info("Publishing log event for task: %s.%s, %s", task_type, task_idx,
                          experiment_name)
        celery_app.send_task(
            RunnerCeleryTasks.EVENTS_HANDLE_LOGS_SIDECAR,
            kwargs={
                'experiment_name': experiment_name,
                'experiment_uuid': experiment_uuid,
                'job_uuid': job_uuid,
                'log_line': log_line,
                'task_type': task_type,
                'task_idx': task_idx})
        try:
            should_stream = (RedisToStream.is_monitored_job_logs(job_uuid) or
                             RedisToStream.is_monitored_experiment_logs(experiment_uuid))
        except RedisError:
            should_stream = False
        if should_stream:
            self._logger.info("Streaming new log event for experiment: %s", experiment_uuid)

            with celery_app.producer_or_acquire(None) as producer:
                try:
                    producer.publish(
                        {
                            'experiment_uuid': experiment_uuid,
                            'job_uuid': job_uuid,
                            'log_line': log_line,
                            'status': status,
                            'task_type': task_type,
                            'task_idx': task_idx
                        },
                        routing_key='{}.{}.{}'.format(RoutingKeys.LOGS_SIDECARS,
                                                      experiment_uuid,
                                                      job_uuid),
                        exchange=settings.INTERNAL_EXCHANGE,
                    )
                except (TimeoutError, AMQPError):
                    pass

    def setup(self):
        import logging

        self._logger = logging.getLogger('polyaxon.monitors.publisher')
