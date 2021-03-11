import logging

import argparse
import random
import time
from urllib import request

import tensorflow as tf
from tensorflow import keras
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from bokeh.plotting import figure
from vega_datasets import data

# Polyaxon
from polyaxon import tracking
from polyaxon.tracking.contrib.keras import PolyaxonKerasCallback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_loss(step):
    result = 10 / (step + 1)
    noise = (random.random() - 0.5) * 0.5 * result
    return result + noise


def get_accuracy(loss):
    return (100 - loss) / 100.0


def get_text(step):
    return 'Some test generated at step {}, this is part of a Polyaxon example.'.format(step)


def get_html(step):
    return (
        '<span><a href="https://link.com">This is a link {step} </a>'
        '<b>Some more html at step {step}</b></span>'.format(step=step)
    )


def log_images(step):
    request.urlretrieve(
        "https://github.com/polyaxon/polyaxon/raw/master/artifacts/logo/profile.png",
        "/tmp/polyaxon.png"
    )
    tracking.log_image("/tmp/polyaxon.png", name='polyaxon-logo', step=step)

    values = np.random.rand(10, 10, 3) * 255
    values = np.repeat(values, 30, 0)
    values = np.repeat(values, 30, 1)
    tracking.log_image(values, name='generated', step=step, dataformats="HWC")

    values = np.random.rand(300, 200, 1) * 255
    tracking.log_image(values, name="3d-gray", step=step, dataformats="HWC")

    values = np.random.rand(300, 200, 3) * 255
    tracking.log_image(values, name="3d-rgb", step=step, dataformats="HWC")

    values = np.random.rand(300, 200, 4) * 255
    tracking.log_image(values, name="3d-rgb-array", step=step, dataformats="HWC")


def get_dist(step):
    x = np.random.random(1000)
    return x + step


def get_audio(step):
    sample_rate = 44100 + step
    freqs = 440
    dummy_audio = np.arange(sample_rate * 2, dtype=np.float32)
    return np.cos(dummy_audio * (2.0 * freqs * np.pi / sample_rate))


def plot_scatter(step):
    x = np.random.randn(1000)
    y = np.random.randn(1000)

    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    plt.figure(figsize=(8, 8))

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
    tracking.log_mpl_plotly_chart(name='scatter', figure=plt, step=step)


def get_sin_plot(step):
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)

    f, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Simple plot')
    tracking.log_mpl_plotly_chart(name='sin', figure=plt, step=step)


def plot_mpl_figure(step):
    np.random.seed(19680801)
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


def log_plotly(step):
    df = px.data.tips()

    fig = px.density_heatmap(df, x="total_bill", y="tip", facet_row="sex", facet_col="smoker")
    tracking.log_plotly_chart(name="2d-hist", figure=fig, step=step)


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
    # TODO: FIX
    tracking.TRACKING_RUN.log_curve(
        name='random-curve-man', x=np.random.randn(100), y=np.random.randn(100), step=step
    )


def train_network():
    data_size = 1000
    # 80% of the data is for training.
    train_pct = 0.8

    train_size = int(data_size * train_pct)

    # Create some input data between -1 and 1 and randomize it.
    x = np.linspace(-1, 1, data_size)
    np.random.shuffle(x)

    # Generate the output data.
    # y = 0.5x + 2 + noise
    y = 0.5 * x + 2 + np.random.normal(0, 0.5, (data_size,))

    # Split into test and train pairs.
    x_train, y_train = x[:train_size], y[:train_size]
    x_test, y_test = x[train_size:], y[train_size:]

    file_writer = tf.summary.create_file_writer(tracking.get_tensorboard_path())
    file_writer.set_as_default()

    def lr_schedule(epoch):
        """
        Returns a custom learning rate that decreases as epochs progress.
        """
        learning_rate = 0.3435
        if epoch > 10:
            learning_rate = 0.0223
        if epoch > 20:
            learning_rate = 0.012
        if epoch > 50:
            learning_rate = 0.00532

        tf.summary.scalar('learning rate', data=learning_rate, step=epoch)
        tracking.log_metric('learning rate', value=learning_rate, step=epoch)
        return learning_rate

    lr_callback = keras.callbacks.LearningRateScheduler(lr_schedule)
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=tracking.get_tensorboard_path())
    plx_callback = PolyaxonKerasCallback(run=tracking.TRACKING_RUN)

    model = keras.models.Sequential([
        keras.layers.Dense(16, input_dim=1),
        keras.layers.Dense(1),
    ])

    model.compile(
        loss='mse',  # keras.losses.mean_squared_error
        optimizer=keras.optimizers.SGD(),
    )

    model.fit(
        x_train,  # input
        y_train,  # output
        batch_size=train_size,
        verbose=0,  # Suppress chatty output; use Tensorboard instead
        epochs=100,
        validation_data=(x_test, y_test),
        callbacks=[tensorboard_callback, lr_callback, plx_callback],
    )


def main():
    tracking.init()

    for i in range(args.steps):
        logger.info('Step %s', i)
        # Scalars
        loss = get_loss(i)
        accuracy = get_accuracy(loss)
        # training metrics, but don't commit the step.
        tracking.log_metrics(step=i, loss=loss, accuracy=accuracy)
        # validation metrics, which could be reported in another part of the code
        if i % args.validate_every == 0:
            tracking.log_metric(name='val_acc', value=accuracy - 0.05, step=i)

        # Dist
        tracking.log_histogram('distribution', get_dist(i), 'auto', step=i)

        # Text
        tracking.log_text('text-ex', text=get_text(i), step=i)

        # images
        log_images(i)
        # HTML
        tracking.log_html('html-ex', html=get_html(i), step=i)

        # Generate sin wave as audio
        tracking.log_audio(data=get_audio(i), name='audio', step=i)

        time.sleep(0.25)

    plot_scatter(100)
    get_sin_plot(100)
    plot_mpl_figure(100)
    log_bokeh(100)
    log_altair(100)
    log_curves(100)
    log_plotly(100)
    log_curves(100)

    train_network()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--steps', type=int, default=100)
    parser.add_argument('--validate_every', type=int, default=10)
    args = parser.parse_args()
    main()
