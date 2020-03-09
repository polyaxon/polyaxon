#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from polyaxon.notifiers.discord_webhook import DiscordWebHookNotifier
from polyaxon.notifiers.hipchat_webhook import HipChatWebHookNotifier
from polyaxon.notifiers.mattermost_webhook import MattermostWebHookNotifier
from polyaxon.notifiers.pagerduty_webhook import PagerDutyWebHookNotifier
from polyaxon.notifiers.slack_webhook import SlackWebHookNotifier
from polyaxon.notifiers.spec import NotificationSpec
from polyaxon.notifiers.webhook import WebHookNotifier

NOTIFIERS = {
    DiscordWebHookNotifier.notification_key: DiscordWebHookNotifier,
    HipChatWebHookNotifier.notification_key: HipChatWebHookNotifier,
    MattermostWebHookNotifier.notification_key: MattermostWebHookNotifier,
    PagerDutyWebHookNotifier.notification_key: PagerDutyWebHookNotifier,
    SlackWebHookNotifier.notification_key: SlackWebHookNotifier,
    WebHookNotifier.notification_key: WebHookNotifier,
}
