from events_handlers.tasks.logger import logger
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import EventsCeleryTasks


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_RESOURCES, ignore_result=True)
def handle_events_resources(payload, persist):
    # here we must persist resources if requested
    logger.info('handling events resources with persist:%s', persist)
    logger.info(payload)
