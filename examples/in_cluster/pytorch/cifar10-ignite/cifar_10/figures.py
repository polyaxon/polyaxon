import numpy as np

# Change matplotlib backend
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns


def create_fig_target_distribution_per_batch(y_counts_df, n_classes_per_fig=20):
    n_classes = y_counts_df.shape[1]
    n = int(np.ceil(n_classes / n_classes_per_fig))
    m = min(3, n)
    k = int(np.ceil(n / m))

    with sns.axes_style("whitegrid"):
        fig, axarr = plt.subplots(k, m, figsize=(10, 10))
        if not isinstance(axarr, np.ndarray):
            axarr = np.array([axarr])
        if axarr.ndim == 1:
            axarr = axarr[None, :]
        for c in range(min(k * m, n)):
            i, j = np.unravel_index(c, dims=(k, m))
            classes = y_counts_df.columns[c * n_classes_per_fig:(c + 1) * n_classes_per_fig]
            axarr[i, j].set_title('Target distribution per batch')
            axarr[i, j].set_xlabel('Count')
            sns.boxplot(data=y_counts_df[classes], orient='h', ax=axarr[i, j])

    return fig


def create_fig_targets_distribution(y_counts_df, n_classes_per_fig=20):
    n_classes = y_counts_df.shape[1]
    n = int(np.ceil(n_classes / n_classes_per_fig))
    m = min(3, n)
    k = int(np.ceil(n / m))
    y_total = y_counts_df.sum(axis=0)

    with sns.axes_style("whitegrid"):
        fig, axarr = plt.subplots(k, m, figsize=(20, 20))
        if not isinstance(axarr, np.ndarray):
            axarr = np.array([axarr])
        if axarr.ndim == 1:
            axarr = axarr[None, :]
        for c in range(min(k * m, n)):
            i, j = np.unravel_index(c, dims=(k, m))
            classes = y_total.index[c * n_classes_per_fig:(c + 1) * n_classes_per_fig]
            axarr[i, j].set_title('Total targets distribution')
            axarr[i, j].set_xlabel('Count')
            sns.barplot(x=y_total[classes], y=classes, orient='h', ax=axarr[i, j])
            axarr[i, j].set_xlim([0, y_total.max() * 1.05])

    return fig


def create_fig_samples_min_avg_max_per_batch(x_stats_df, min_cols, avg_cols, max_cols):
    n_channels = len(min_cols)
    fig, axarr = plt.subplots(n_channels, 3, figsize=(20, 20))
    if not isinstance(axarr, np.ndarray):
        axarr = np.array([axarr])
    if axarr.ndim == 1:
        axarr = axarr[None, :]
    fig.suptitle("Sample min/avg/max per bands")

    with sns.axes_style("whitegrid"):
        for i in range(n_channels):
            for j, col in enumerate([min_cols, avg_cols, max_cols]):
                axarr[i, j].set_title(col[i])
                axarr[i, j].hist(x_stats_df[col[i]], bins=100)
    return fig


def create_fig_samples_param_per_batch(x_stats_df, param_name):
    fig = plt.figure(figsize=(10, 10))
    ax = plt.subplot(1, 1, 1)
    sns.countplot(data=x_stats_df, x=param_name, ax=ax)
    return fig


def create_fig_param_per_class(param_values, param_name, classes=None, n_classes_per_fig=20):
    n_classes = len(param_values)
    if classes is None:
        classes = np.array(["class_{}".format(i) for i in range(n_classes)])
    with sns.axes_style("whitegrid"):
        n = int(np.ceil(n_classes / n_classes_per_fig))
        m = min(3, n)
        k = int(np.ceil(n / m))
        fig, axarr = plt.subplots(k, m, figsize=(20, 20))
        if not isinstance(axarr, np.ndarray):
            axarr = np.array([axarr])
        if axarr.ndim == 1:
            axarr = axarr[None, :]
        max_val = param_values.max() * 1.05
        for c in range(min(k * m, n)):
            i, j = np.unravel_index(c, dims=(k, m))
            batch_classes = classes[c * n_classes_per_fig:(c + 1) * n_classes_per_fig]
            batch_param_values = param_values[c * n_classes_per_fig:(c + 1) * n_classes_per_fig]
            axarr[i, j].set_title('{} per class'.format(param_name))
            axarr[i, j].set_xlabel('{}'.format(param_name))
            sns.barplot(y=batch_classes, x=batch_param_values, ax=axarr[i, j])
            axarr[i, j].set_xlim([0, max_val])
    return fig
