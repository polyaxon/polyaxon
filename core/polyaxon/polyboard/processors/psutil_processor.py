# !/usr/bin/python
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

from typing import Dict, List

from polyaxon.polyboard.processors.events_processors import metrics_dict_to_list

try:
    import psutil
except ImportError:
    psutil = None


def can_log_psutil_resources():
    return psutil is not None


def query_psutil() -> Dict:
    vm = psutil.virtual_memory()
    results = {}
    percents = psutil.cpu_percent(interval=None, percpu=True)
    if len(percents) > 0:
        results["cpu_percent_avg"] = sum(percents) / len(percents)
        for (i, percent) in enumerate(percents):
            results["cpu_percent_%02d" % (i + 1)] = percent
    try:
        # psutil <= 5.6.2 did not have getloadavg:
        if hasattr(psutil, "getloadavg"):
            results["load_avg"] = psutil.getloadavg()[0]
        else:
            # Do not log an empty metric
            pass
    except OSError:
        pass
    results["memory_used"] = vm.used / vm.total
    return results


def get_psutils_metrics() -> List:
    return metrics_dict_to_list(query_psutil())
