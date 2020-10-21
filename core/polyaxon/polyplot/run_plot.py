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
import pandas as pd

from typing import Dict, List, Set, Union

from polyaxon.client import RunClient
from polyaxon.client.decorators import check_no_op
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyboard.events import V1Events


class RunPlot(RunClient):
    @check_no_op
    def __init__(
        self,
        owner=None,
        project=None,
        run_uuid=None,
        client=None,
    ):
        super().__init__(owner=owner, project=project, run_uuid=run_uuid, client=client)
        self.metrics = {}
        self.metric_names = set([])

    @check_no_op
    def refresh_data(self, force: bool = False):
        super().refresh_data()
        if self.metrics:
            self.get_metrics(self.metric_names, force)

    @check_no_op
    def get_metrics(
        self, names: Union[Set[str], List[str]], force: bool = False
    ) -> Dict:
        events = self.get_events(
            kind=V1ArtifactKind.METRIC,
            names=names,
            orient=V1Events.ORIENT_DICT,
            force=force,
        ).data
        for e in events:
            self.metrics[e["name"]] = e
            self.metric_names.add(e["name"])
        return self.metrics

    @check_no_op
    def get_tidy_df(self):
        dfs = []
        for m in self.metric_names:
            data = self.metrics[m]
            df = V1Events.read(**data).df
            df["name"] = m
            dfs.append(df)
        return pd.concat(dfs)

    @check_no_op
    def get_wide_df(self):
        dfs = []
        for m in self.metric_names:
            data = self.metrics[m]
            df = V1Events.read(**data).df
            df[m] = df.metric
            df = df[["step", "timestamp", m]]
            dfs.append(df)

        return pd.concat(dfs, axis=1)

    @check_no_op
    def bar(
        self,
        x: str = "timestamp",
        y: str = "metric",
        color: str = "name",
        barmode: str = "group",
    ):
        import plotly.express as px

        df = self.get_tidy_df()
        return px.bar(df, x=x, y=y, color=color, barmode=barmode)

    @check_no_op
    def line(self, x: str = "timestamp", y: str = "metric", color: str = "name"):
        import plotly.express as px

        df = self.get_tidy_df()
        return px.line(df, x=x, y=y, color=color)

    @check_no_op
    def scatter(self, x: str = None, y: str = None, color: str = None, **kwargs):
        import plotly.express as px

        if len(self.metric_names) < 2:
            raise ValueError("You need at least 2 metrics to use this plot.")

        df = self.get_wide_df()
        return px.scatter(df, x=x, y=y, color=color, **kwargs)


class MultiRunPlot(RunClient):
    @check_no_op
    def __init__(
        self,
        owner=None,
        project=None,
        client=None,
    ):
        super().__init__(owner=owner, project=project, client=client)
        self.runs = {}
        self.run_uuids = set([])
        self.metric_names = set([])

    @check_no_op
    def refresh_data(self):
        super().refresh_data()
        if self.runs:
            self.get_runs(query="uuid:".format("|".join(self.run_uuids)))
            if self.metric_names:
                self.get_metrics(self.metric_names)

    @check_no_op
    def get_metrics(
        self, names: Union[Set[str], List[str]], force: bool = False
    ) -> Dict:
        events = self.get_events(
            kind=V1ArtifactKind.METRIC,
            names=names,
            orient=V1Events.ORIENT_DICT,
            force=force,
        ).data
        for e in events:
            self.metrics[e["name"]] = e
            self.metric_names.add(e["name"])

        return self.metrics

    @check_no_op
    def get_runs(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ) -> Dict:
        runs = self.list(
            query=query,
            sort=sort,
            limit=limit,
            offset=offset,
        ).results
        for r in runs:
            self.run_uuids.add(r.uuid)
            self.runs[r.uuid] = r
        return self.runs

    def get_runs_io(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        runs = self.get_runs(query=query, sort=sort, limit=limit, offset=offset)
        data = []
        for r in runs:
            run = runs[r]
            values = run.inputs or {}
            values.update(run.outputs or {})
            data.append({"uid": run.uuid, "values": values})
        return data

    @check_no_op
    def get_hiplot(
        self, query: str = None, sort: str = None, limit: int = None, offset: int = None
    ):
        import hiplot

        data = self.get_runs_io(query=query, sort=sort, limit=limit, offset=offset)
        exp = hiplot.Experiment()
        for d in data:
            dp = hiplot.Datapoint(uid=d["uid"], values=d["values"])
            exp.datapoints.append(dp)
        return exp
