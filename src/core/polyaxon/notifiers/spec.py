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
# limitations under the License

from collections import namedtuple
from typing import Optional

from polyaxon.lifecycle import StatusColor
from polyaxon.utils.urls_utils import get_run_url


class NotificationSpec(
    namedtuple(
        "Notification",
        "kind owner project uuid name status wait_time duration condition inputs outputs",
    )
):
    def get_details(self) -> str:
        details = "{} ({})".format(self.name, self.uuid) if self.name else self.uuid
        details = "Run: {}\n".format(details)
        if self.kind:
            details = "Kind: `{}`\n".format(self.kind)
        details += "Status: `{}`\n".format(self.status)
        if self.condition.reason:
            details += "Reason: `{}`\n".format(self.condition.reason)
        if self.condition.message:
            details += "Message: `{}`\n".format(self.condition.message)
        details += "Transition time: `{}`\n".format(self.condition.last_transition_time)
        if self.wait_time:
            details += "Wait time: `{}`\n".format(self.wait_time)
        if self.duration:
            details += "Duration: `{}`\n".format(self.duration)
        if self.inputs:
            details += "Inputs: `{}`\n".format(self.inputs)
        if self.outputs:
            details += "Outputs: `{}`\n".format(self.outputs)

        return details

    def get_title(self) -> str:
        details = "{} ({})".format(self.name, self.uuid) if self.name else self.uuid
        details += " Status: {}\n".format(self.status)
        return details

    def get_color(self) -> str:
        return StatusColor.get_color(self.condition.type)

    def get_url_path(self) -> Optional[str]:
        if self.owner and self.project and self.uuid:
            uri = get_run_url(
                owner=self.owner, project_name=self.project, run_uuid=self.uuid
            )
            return "ui{}".format(uri)
