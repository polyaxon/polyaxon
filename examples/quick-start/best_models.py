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

import argparse

from polyaxon.client import RunClient


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--project',
        type=str
    )
    parser.add_argument(
        '--top',
        type=int
    )
    args = parser.parse_args()

    project = args.project

    client = RunClient()

    print("Top 5 experiment based on accuracy for project {}: ".format(project))
    for run in client.list(
        query="metrics.accuracy:>0.9, project.name:{}".format(project),
        sort="-metrics.accuracy",
        limit=args.top
    ):
        print("Run", run.run_data.uuid, run.run_data.name)
        print("Inputs", run.get_inputs())
        print("Outputs", run.get_outputs())
