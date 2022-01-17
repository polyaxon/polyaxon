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

from marshmallow import fields

_date_field = fields.Date()
date_deserialize = _date_field.deserialize
date_serialize = _date_field.serialize

_datetime_field = fields.DateTime()
datetime_deserialize = _datetime_field.deserialize
datetime_serialize = _datetime_field.serialize

_timedelta_field = fields.TimeDelta()
timedelta_deserialize = _timedelta_field.deserialize
timedelta_serialize = _timedelta_field.serialize

_uuid_field = fields.UUID(format="hex")
uuid_deserialize = _uuid_field.deserialize
uuid_serialize = _uuid_field.serialize
