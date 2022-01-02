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

from requests import RequestException
from typing import Dict, List

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.logger import logger
from polyaxon.notifiers.base import BaseNotifier
from polyaxon.notifiers.keys import INTEGRATIONS_WEBHOOKS_GENERIC
from polyaxon.notifiers.spec import NotificationSpec
from polyaxon.utils.requests_utils import safe_request


class WebHookNotifier(BaseNotifier):
    notification_key = V1ConnectionKind.WEBHOOK
    name = "WebHook"
    description = (
        "Webhooks send an HTTP payload to the webhook's configured URL."
        "Webhooks can be used automatically "
        "by subscribing to certain events on Polyaxon, "
        "or manually triggered by a user operation."
    )
    raise_empty_context = False
    config_key = INTEGRATIONS_WEBHOOKS_GENERIC

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        context = {
            "owner": notification.uuid,
            "project": notification.uuid,
            "uuid": notification.uuid,
            "name": notification.name,
            "title": notification.get_title(),
            "details": notification.get_details(),
            "finished_at": notification.condition.last_transition_time,
        }
        return context

    @classmethod
    def _pre_execute_web_hook(cls, data: Dict, config: Dict) -> Dict:
        return data

    @classmethod
    def _execute(cls, data: Dict, config: List[Dict]) -> None:
        for web_hook in config:
            data = cls._pre_execute_web_hook(data=data, config=web_hook)
            try:
                if web_hook["method"] == "POST":
                    safe_request(
                        url=web_hook["url"], method=web_hook["method"], json=data
                    )
                else:
                    safe_request(
                        url=web_hook["url"], method=web_hook["method"], params=data
                    )
            except RequestException:
                logger.warning("Could not send web hook, exception.", exc_info=True)
