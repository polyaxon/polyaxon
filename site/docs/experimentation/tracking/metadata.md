---
title: "Tracking Metadata & Events"
sub_link: "tracking/metadata"
meta_title: "Add graphs and events tracking and log metadata to the lineage table - Tracking - Experimentation"
meta_description: "Tracking graphs and events and log metadata lineage related to files and assets."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
  - tracking
  - reference
  - sdk
sidebar: "experimentation"
---

Polyaxon provides several methods for tracking metrics, metadata, summaries, and graphs in your jobs.

## Overview

For each run, Polyaxon creates an artifacts folder with a predefined structure to organize your events:

 * metrics
 * charts
 * text
 * HTML
 * ...

Some events create save related assets to these events and are saved under a separate folder called `assets`.

## Logging single results and outputs

To log single results that do not need to be visualized, do not change over time, 
or only should be recorded at the end of a job you should use:

```python
from polyaxon import tracking

tracking.log_outputs(foo="bar", scalar=0.1, key="val")
``` 

## Logging step-wise events

To log texts, HTML, scalars, metrics that change overtime or need to be recorded in a step-wise manner, or if you need to visualize the event in the dashboard you should use:

### Tracking changing metrics

```python
from polyaxon import tracking

def get_loss(step):
    result = 10 / (step + 1)
    noise = (random.random() - 0.5) * 0.5 * result
    return result + noise

def get_accuracy(loss):
    return (100 - loss) / 100.0

for i in range(1, 5):
    loss = get_loss(i)
    accuracy = get_accuracy(loss)
    tracking.log_metrics(loss=loss, accuracy=accuracy, step=i)
```
 
### Tracking a changing text value over time or step-wise

```python
from polyaxon import tracking

for i in range(1, 5):
    tracking.log_text(name="text-event", value="value at step {}".format(i), step=i)
```
 
### Tracking a changing HTML value over time or step-wise

```python
from polyaxon import tracking

def get_html(step):
    return (
        '<span><a href="https://link.com">This is a link {step} </a>'
        '<b>Some more html at step {step}</b></span>'.format(step=step)
    )

for i in range(1, 5):
    tracking.log_html(name="text-event", html=get_html(i), step=i)
```

### Tracking a changing audio over time or step-wise
 
```python
import numpy as np

from polyaxon import tracking

def get_audio(step):
    sample_rate = 44100 + step
    freqs = 440
    dummy_audio = np.arange(sample_rate * 2, dtype=np.float32)
    return np.cos(dummy_audio * (2.0 * freqs * np.pi / sample_rate))

for i in range(1, 5):
    tracking.log_audio(data=get_audio(i), name='audio-ex', step=i)
```
 
### Tracking a changing distribution over time or step-wise


```python
from polyaxon import tracking

def get_dist(step):
    x = np.random.random(1000)
    return x + step


def get_np_hist(step):
    values, counts = np.histogram(np.random.randint(255, size=(1000,)))
    return {"values": values, "counts": counts, "step": step}

for i in range(1, 5):
    tracking.log_histogram('distribution', get_dist(i), 'auto', step=i)
    tracking.log_np_histogram('np-hist', **get_np_hist(i))
```

 * Tracking a changing curves and charts over time or step-wise

```python
import random

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from bokeh.plotting import figure
from vega_datasets import data

from polyaxon import tracking


def plot_scatter(step):
    x = np.random.randn(step)
    y = np.random.randn(step)

    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    figure = plt.figure(figsize=(8, 8))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    ax_histx = plt.axes(rect_histx)
    ax_histx.tick_params(direction='in', labelbottom=False)
    ax_histy = plt.axes(rect_histy)
    ax_histy.tick_params(direction='in', labelleft=False)
    ax_scatter.scatter(x, y)

    binwidth = 0.25
    lim = np.ceil(np.abs([x, y]).max() / binwidth) * binwidth
    ax_scatter.set_xlim((-lim, lim))
    ax_scatter.set_ylim((-lim, lim))

    bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins)
    ax_histy.hist(y, bins=bins, orientation='horizontal')

    ax_histx.set_xlim(ax_scatter.get_xlim())
    ax_histy.set_ylim(ax_scatter.get_ylim())
    tracking.log_mpl_plotly_chart(name='scatter', figure=figure, step=step)


def plot_mpl_figure(step):
    np.random.seed(step)
    data = np.random.randn(2, 100)

    figure, axs = plt.subplots(2, 2, figsize=(5, 5))
    axs[0, 0].hist(data[0])
    axs[1, 0].scatter(data[0], data[1])
    axs[0, 1].plot(data[0], data[1])
    axs[1, 1].hist2d(data[0], data[1])

    tracking.log_mpl_image(figure, 'mpl_image', step=step)


def log_bokeh(step):
    factors = ["a", "b", "c", "d", "e", "f", "g", "h"]
    x = [50, 40, 65, 10, 25, 37, 80, 60]

    dot = figure(title="Categorical Dot Plot", tools="", toolbar_location=None,
                 y_range=factors, x_range=[0, 100])

    dot.segment(0, factors, x, factors, line_width=2, line_color="green", )
    dot.circle(x, factors, size=15, fill_color="orange", line_color="green", line_width=3, )

    factors = ["foo 123", "bar:0.2", "baz-10"]
    x = ["foo 123", "foo 123", "foo 123", "bar:0.2", "bar:0.2", "bar:0.2", "baz-10", "baz-10",
         "baz-10"]
    y = ["foo 123", "bar:0.2", "baz-10", "foo 123", "bar:0.2", "baz-10", "foo 123", "bar:0.2",
         "baz-10"]
    colors = [
        "#0B486B", "#79BD9A", "#CFF09E",
        "#79BD9A", "#0B486B", "#79BD9A",
        "#CFF09E", "#79BD9A", "#0B486B"
    ]

    hm = figure(title="Categorical Heatmap", tools="hover", toolbar_location=None,
                x_range=factors, y_range=factors)

    hm.rect(x, y, color=colors, width=1, height=1)

    tracking.log_bokeh_chart(name='confusion-bokeh', figure=hm, step=step)


def log_altair(step):
    source = data.cars()

    brush = alt.selection(type='interval')

    points = alt.Chart(source).mark_point().encode(
        x='Horsepower:Q',
        y='Miles_per_Gallon:Q',
        color=alt.condition(brush, 'Origin:N', alt.value('lightgray'))
    ).add_selection(
        brush
    )

    bars = alt.Chart(source).mark_bar().encode(
        y='Origin:N',
        color='Origin:N',
        x='count(Origin):Q'
    ).transform_filter(
        brush
    )

    chart = points & bars

    tracking.log_altair_chart(name='altair_chart', figure=chart, step=step)


def log_curves(step):
    # ROC curve
    x = [
        0.0,
        0.0,
        0.0,
        0.0196078431372549,
        0.0196078431372549,
        0.0784313725490196,
        0.0784313725490196,
        0.09803921568627451,
        0.09803921568627451,
        0.11764705882352941,
        0.11764705882352941,
        0.13725490196078433,
        0.13725490196078433,
        0.1568627450980392,
        0.1568627450980392,
        0.17647058823529413,
        0.17647058823529413,
        0.3137254901960784,
        0.3137254901960784,
        0.3333333333333333,
        0.3333333333333333,
        0.35294117647058826,
        0.35294117647058826,
        0.4117647058823529,
        0.4117647058823529,
        0.45098039215686275,
        0.45098039215686275,
        0.47058823529411764,
        0.47058823529411764,
        0.5098039215686274,
        0.5098039215686274,
        0.5686274509803921,
        0.5686274509803921,
        1.0
    ]
    y = [
        0.0,
        0.041666666666666664,
        0.125,
        0.125,
        0.25,
        0.25,
        0.2916666666666667,
        0.2916666666666667,
        0.3333333333333333,
        0.3333333333333333,
        0.4166666666666667,
        0.4166666666666667,
        0.5,
        0.5,
        0.5416666666666666,
        0.5416666666666666,
        0.5833333333333334,
        0.5833333333333334,
        0.7083333333333334,
        0.7083333333333334,
        0.75,
        0.75,
        0.7916666666666666,
        0.7916666666666666,
        0.8333333333333334,
        0.8333333333333334,
        0.875,
        0.875,
        0.9166666666666666,
        0.9166666666666666,
        0.9583333333333334,
        0.9583333333333334,
        1.0,
        1.0
    ]
    tracking.log_roc_auc_curve(name='roc-curve-man', fpr=x, tpr=y, auc=0.742149, step=step)

    x = [0.66666667, 0.5, 1., 1.]
    y = [1., 0.5, 0.5, 0.]
    tracking.log_pr_curve(name='pr-curve-man', precision=x, recall=y, average_precision=0.742149,
                          step=step)

    # Random curve
    tracking.log_curve(
        name='random-curve-man', x=np.random.randn(10 * step), y=np.random.randn(10 * step), step=step
    )



def get_sin_plot(step):
    x = np.linspace(0, step * np.pi, 400)
    y = np.sin(x ** 2)

    f, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Simple plot')
    tracking.log_mpl_plotly_chart(name='sin', figure=f, step=step)


def log_confusion(step):
    z = np.array([[0.1, 0.3, 0.5, 0.2],
     [1.0, 0.8, 0.6, 0.1],
     [0.1, 0.3, 0.6, 0.9],
     [0.6, 0.4, 0.2, 0.2]]) * step

    x = ['healthy', 'multiple diseases', 'rust', 'scab']
    y = ['healthy', 'multiple diseases', 'rust', 'scab']
    tracking.log_confusion_matrix("confusion_test", x, y, z.tolist(), step=step)


def log_plotly(step):
    df = px.data.tips()

    fig = px.density_heatmap(df, x="total_bill", y="tip", facet_row="sex", facet_col="smoker")
    tracking.log_plotly_chart(name="2d-hist", figure=fig, step=step)


for i in range(1, 5):
    plot_scatter(i)
    get_sin_plot(i)
    plot_mpl_figure(i)
    log_bokeh(i)
    log_altair(i)
    log_curves(i)
    log_plotly(i)
    log_confusion(i)
```
