#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polyaxon.constants.globals import UNKNOWN
from polyaxon.utils.path_utils import module_type
from traceml.events import V1EventChart, V1EventChartKind
from traceml.logger import logger
from traceml.processors.errors import (
    BOKEH_ERROR_MESSAGE,
    MATPLOTLIB_ERROR_MESSAGE,
    PLOTLY_ERROR_MESSAGE,
)

try:
    import numpy as np
except ImportError:
    np = None


def bokeh_chart(figure) -> V1EventChart:
    try:
        from bokeh.embed import json_item
    except ImportError:
        logger.warning(BOKEH_ERROR_MESSAGE)
        return UNKNOWN
    return V1EventChart(kind=V1EventChartKind.BOKEH, figure=json_item(figure))


def altair_chart(figure) -> V1EventChart:
    return V1EventChart(kind=V1EventChartKind.VEGA, figure=figure.to_dict())


def plotly_chart(figure) -> V1EventChart:
    try:
        import plotly.tools

        from traceml.vendor.matplotlylib import mpl_to_plotly
    except ImportError:
        logger.warning(PLOTLY_ERROR_MESSAGE)
        return UNKNOWN

    if module_type(figure, "matplotlib.figure.Figure"):
        figure = mpl_to_plotly(figure)
    else:
        figure = plotly.tools.return_figure_from_figure_or_data(
            figure, validate_figure=True
        )
    return V1EventChart(kind=V1EventChartKind.PLOTLY, figure=figure)


def mpl_plotly_chart(figure, close: bool = True) -> V1EventChart:
    try:
        import plotly.tools

        from plotly import optional_imports
    except ImportError:
        logger.warning(PLOTLY_ERROR_MESSAGE)
        return UNKNOWN

    try:
        import matplotlib
        import matplotlib.pyplot as plt

        from matplotlib.figure import Figure
    except ImportError:
        logger.warning(MATPLOTLIB_ERROR_MESSAGE)

    if module_type(figure, "matplotlib.figure.Figure"):
        pass
    else:
        if figure == matplotlib.pyplot:
            figure = figure.gcf()
        elif not isinstance(figure, Figure):
            if hasattr(figure, "figure"):
                figure = figure.figure
                # Some matplotlib objects have a figure function
                if not isinstance(figure, Figure):
                    raise ValueError(
                        "Only matplotlib.pyplot or matplotlib.pyplot.Figure objects are accepted."
                    )

    from traceml.vendor.matplotlylib import mpl_to_plotly

    plotly_figure = mpl_to_plotly(figure)
    result = plotly_chart(figure=plotly_figure)
    if close:
        try:
            plt.close(figure.number)
        except Exception:  # noqa
            plt.close(figure)

    return result
