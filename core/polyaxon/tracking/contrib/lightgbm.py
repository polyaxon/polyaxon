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

from polyaxon import tracking


def polyaxon_callback(run=None):
    run = tracking.get_or_create_run(run)

    def callback(env):
        res = {}
        for data_name, eval_name, value, _ in env.evaluation_result_list:
            key = data_name + "-" + eval_name
            res[key] = value
        run.log_metrics(step=env.iteration, **res)

    return callback
