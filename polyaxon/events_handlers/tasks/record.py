from django.db import IntegrityError

import auditor
import workers

from polyaxon.settings import EventsCeleryTasks


@workers.app.task(name=EventsCeleryTasks.EVENTS_NOTIFY, ignore_result=True)
def events_notify(event: 'Event') -> None:
    auditor.notify(event)


@workers.app.task(name=EventsCeleryTasks.EVENTS_LOG,
                  autoretry_for=(IntegrityError,),
                  max_retries=3,
                  ignore_result=True)
def events_log(event: 'Event') -> None:
    auditor.log(event)


@workers.app.task(name=EventsCeleryTasks.EVENTS_TRACK, ignore_result=True)
def events_track(event: 'Event') -> None:
    auditor.track(event)
