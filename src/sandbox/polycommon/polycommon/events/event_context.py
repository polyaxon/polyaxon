#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import namedtuple
from typing import Any, Optional

from polyaxon.utils.http_utils import absolute_uri
from polyaxon.utils.urls_utils import get_fqn_run_url, get_owner_url, get_project_url
from polycommon import user_system
from polycommon.events import event_subjects


class EventItemContextSpec(namedtuple("EventItemContextSpec", "name url object_id")):
    pass


class EventContextSpec(
    namedtuple(
        "EventItemContextSpec",
        "subject_action subject action actor_context object_context datetime",
    )
):
    pass


def get_event_subject(event_type: str) -> str:
    """Return the first part of the event_type

    e.g.

    >>> Event.event_type = 'experiment.deleted'
    >>> Event.get_event_subject() == 'experiment'
    """
    return event_type.split(".")[0]


def get_event_action(event_type: str) -> str:
    """Return the second part of the event_type

    e.g.

    >>> Event.event_type = 'experiment.deleted'
    >>> Event.get_event_action() == 'deleted'
    """
    return event_type.split(".")[1]


def get_event_actor_context(
    event: "Event",  # noqa: F821
) -> Optional[EventItemContextSpec]:
    if not event.actor:
        return None

    username = event.data.get(event.actor_name)
    if username is None:
        return None
    if username == user_system.USER_SYSTEM_NAME:
        return EventItemContextSpec(name=username, url="/", object_id=None)
    return EventItemContextSpec(
        name=username, url=get_owner_url(username), object_id=None
    )


def get_event_object_context(
    event_content_object: Any, event_type: str
) -> Optional[EventItemContextSpec]:
    # Deleted objects don't have a content object any more
    if not event_content_object:
        return EventItemContextSpec(name=None, url=None, object_id=None)

    event_subject = get_event_subject(event_type)

    object_id = None
    object_url = None
    object_name = None
    if hasattr(event_content_object, "id"):
        object_id = event_content_object.id

    if hasattr(event_content_object, "unique_name"):
        object_name = event_content_object.unique_name
        if event_subject == event_subjects.PROJECT:
            object_url = get_project_url(object_name)
        elif event_subject == event_subjects.RUN:
            object_url = get_fqn_run_url(object_name)

    elif hasattr(event_content_object, "name"):
        object_name = event_content_object.name
    elif hasattr(event_content_object, "username"):
        object_name = event_content_object.username
        object_url = get_owner_url(event_content_object.username)

    # Set proper url
    object_url = absolute_uri("ui{}".format(object_url))
    return EventItemContextSpec(name=object_name, url=object_url, object_id=object_id)


def get_event_context(event: "Event") -> EventContextSpec:  # noqa: F821
    subject = get_event_subject(event_type=event.event_type)
    action = get_event_action(event_type=event.event_type)
    actor_context = get_event_actor_context(event=event)
    object_context = get_event_object_context(
        event_content_object=event.instance, event_type=event.event_type
    )
    return EventContextSpec(
        subject_action="{} {}".format(subject, action),
        subject=subject,
        action=action,
        actor_context=actor_context,
        object_context=object_context,
        datetime=event.datetime,
    )


def get_readable_event(event_context: EventContextSpec) -> str:
    description = "{} on {}".format(
        event_context.subject_action, event_context.datetime
    )
    if event_context.actor_context:
        description += "\nActor: [{}]({})".format(
            event_context.actor_context.name, event_context.actor_context.url
        )

    if event_context.object_context.name and event_context.object_context.url:
        description += "\nObject: [{}]({})".format(
            event_context.object_context.name, event_context.object_context.url
        )

    return description
