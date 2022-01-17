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
import io

from typing import Dict, List

from polyaxon.constants.globals import UNKNOWN
from polyaxon.logger import logger
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyboard.events import (
    LoggedEventSpec,
    V1Event,
    V1EventArtifact,
    V1EventAudio,
    V1EventChart,
    V1EventChartKind,
    V1EventConfusionMatrix,
    V1EventCurve,
    V1EventCurveKind,
    V1EventDataframe,
    V1EventHistogram,
    V1EventImage,
    V1EventModel,
    V1EventVideo,
)
from polyaxon.utils.np_utils import calculate_scale_factor, to_np
from polyaxon.utils.path_utils import (
    check_or_create_path,
    copy_file_or_dir_path,
    copy_file_path,
    module_type,
)

try:
    import numpy as np
except ImportError:
    np = None


NUMPY_ERROR_MESSAGE = "numpy is required for this tracking operation!"
PIL_ERROR_MESSAGE = "PIL/Pillow is required for this tracking operation!"
MOVIEPY_ERROR_MESSAGE = "moviepy is required for this tracking operation!"
MATPLOTLIB_ERROR_MESSAGE = "matplotlib is required for this tracking operation!"
PLOTLY_ERROR_MESSAGE = "plotly is required for this tracking operation!"
BOKEH_ERROR_MESSAGE = "bokeh is required for this tracking operation!"
SKLEARN_ERROR_MESSAGE = "sklearn is required for this tracking operation!"


def dataframe_path(
    from_path: str,
    asset_path: str,
    content_type: str = None,
    asset_rel_path: str = None,
) -> V1EventDataframe:
    copy_file_path(from_path, asset_path)
    return V1EventDataframe(
        path=asset_rel_path or asset_path, content_type=content_type
    )


def model_path(
    from_path: str,
    asset_path: str,
    framework: str = None,
    spec: Dict = None,
    asset_rel_path: str = None,
) -> V1EventModel:
    copy_file_or_dir_path(from_path, asset_path)
    return V1EventModel(
        path=asset_rel_path or asset_path, framework=framework, spec=spec
    )


def artifact_path(
    from_path: str, asset_path: str, kind: str, asset_rel_path: str = None
) -> V1EventArtifact:
    copy_file_or_dir_path(from_path, asset_path)
    return V1EventArtifact(kind=kind, path=asset_rel_path or asset_path)


def image_path(
    from_path: str, asset_path: str, asset_rel_path: str = None
) -> V1EventImage:
    copy_file_path(from_path, asset_path)
    return V1EventImage(path=asset_rel_path or asset_path)


def video_path(
    from_path: str, asset_path: str, content_type=None, asset_rel_path: str = None
) -> V1EventVideo:
    copy_file_path(from_path, asset_path)
    return V1EventVideo(path=asset_rel_path or asset_path, content_type=content_type)


def audio_path(
    from_path: str, asset_path: str, content_type=None, asset_rel_path: str = None
) -> V1EventAudio:
    copy_file_path(from_path, asset_path)
    return V1EventAudio(path=asset_rel_path or asset_path, content_type=content_type)


def _draw_single_box(
    image,
    xmin,
    ymin,
    xmax,
    ymax,
    display_str,
    color="black",
    color_text="black",
    thickness=2,
):
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    try:
        from PIL import ImageDraw, ImageFont
    except ImportError:
        logger.warning(PIL_ERROR_MESSAGE)
        return UNKNOWN

    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
    draw.line(
        [(left, top), (left, bottom), (right, bottom), (right, top), (left, top)],
        width=thickness,
        fill=color,
    )
    if display_str:
        text_bottom = bottom
        # Reverse list and print from bottom to top.
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle(
            [
                (left, text_bottom - text_height - 2 * margin),
                (left + text_width, text_bottom),
            ],
            fill=color,
        )
        draw.text(
            (left + margin, text_bottom - text_height - margin),
            display_str,
            fill=color_text,
            font=font,
        )
    return image


def metric(value):
    if isinstance(value, float):
        return value

    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    value = to_np(value)
    assert value.squeeze().ndim == 0, "scalar should be 0D"
    return float(value)


def histogram(values, bins, max_bins=None):
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    values = to_np(values).astype(float)

    if values.size == 0:
        raise ValueError("The input has no element.")
    values = values.reshape(-1)
    counts, limits = np.histogram(values, bins=bins)
    num_bins = len(counts)
    if max_bins is not None and num_bins > max_bins:
        subsampling = num_bins // max_bins
        subsampling_remainder = num_bins % subsampling
        if subsampling_remainder != 0:
            counts = np.pad(
                counts,
                pad_width=[[0, subsampling - subsampling_remainder]],
                mode="constant",
                constant_values=0,
            )
        counts = counts.reshape(-1, subsampling).sum(axis=-1)

    if counts.size == 0:
        logger.warning("Tracking an empty histogram")
        return UNKNOWN

    return V1EventHistogram(values=values, counts=counts)


def np_histogram(values, counts):
    return V1EventHistogram(values=values, counts=counts)


def encoded_image(asset_path: str, data, asset_rel_path: str = None):
    try:
        from PIL import Image
    except ImportError:
        logger.warning(PIL_ERROR_MESSAGE)
        return UNKNOWN

    image_data = Image.open(io.BytesIO(data.encoded_image_string))
    return save_image(
        asset_path=asset_rel_path or asset_path,
        image_data=image_data,
        height=data.height,
        width=data.width,
        colorspace=data.colorspace,
    )


def image(
    asset_path: str, data, rescale=1, dataformats="CHW", asset_rel_path: str = None
):
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    tensor = to_np(data)
    tensor = convert_to_HWC(tensor, dataformats)
    # Do not assume that user passes in values in [0, 255], use data type to detect
    scale_factor = calculate_scale_factor(tensor)
    tensor = tensor.astype(np.float32)
    tensor = (tensor * scale_factor).astype(np.uint8)
    return make_image(
        asset_path, tensor, rescale=rescale, asset_rel_path=asset_rel_path
    )


def image_boxes(
    asset_path: str,
    tensor_image,
    tensor_boxes,
    rescale=1,
    dataformats="CHW",
    asset_rel_path: str = None,
):
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    tensor_image = to_np(tensor_image)
    tensor_image = convert_to_HWC(tensor_image, dataformats)
    tensor_boxes = to_np(tensor_boxes)
    tensor_image = tensor_image.astype(np.float32) * calculate_scale_factor(
        tensor_image
    )
    return make_image(
        asset_path,
        tensor_image.astype(np.uint8),
        rescale=rescale,
        rois=tensor_boxes,
        asset_rel_path=asset_rel_path,
    )


def draw_boxes(disp_image, boxes):
    # xyxy format
    num_boxes = boxes.shape[0]
    list_gt = range(num_boxes)
    for i in list_gt:
        disp_image = _draw_single_box(
            disp_image,
            boxes[i, 0],
            boxes[i, 1],
            boxes[i, 2],
            boxes[i, 3],
            display_str=None,
            color="Red",
        )
    return disp_image


def make_image(
    asset_path: str, tensor, rescale=1, rois=None, asset_rel_path: str = None
):
    try:
        from PIL import Image
    except ImportError:
        logger.warning(PIL_ERROR_MESSAGE)
        return UNKNOWN

    height, width, colorspace = tensor.shape
    scaled_height = int(height * rescale)
    scaled_width = int(width * rescale)
    image_data = Image.fromarray(tensor)
    if rois is not None:
        image_data = draw_boxes(image_data, rois)
    image_data = image_data.resize((scaled_width, scaled_height), Image.ANTIALIAS)

    return save_image(
        asset_path=asset_path,
        image_data=image_data,
        height=height,
        width=width,
        colorspace=colorspace,
        asset_rel_path=asset_rel_path,
    )


def save_image(
    asset_path: str, image_data, height, width, colorspace, asset_rel_path: str = None
):
    check_or_create_path(asset_path, is_dir=False)
    image_data.save(asset_path, format="PNG")
    return V1EventImage(
        height=height,
        width=width,
        colorspace=colorspace,
        path=asset_rel_path or asset_path,
    )


def video(
    asset_path: str, tensor, fps=4, content_type="gif", asset_rel_path: str = None
):
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    tensor = to_np(tensor)
    tensor = prepare_video(tensor)
    # If user passes in uint8, then we don't need to rescale by 255
    scale_factor = calculate_scale_factor(tensor)
    tensor = tensor.astype(np.float32)
    tensor = (tensor * scale_factor).astype(np.uint8)
    return make_video(
        asset_path, tensor, fps, content_type, asset_rel_path=asset_rel_path
    )


def make_video(
    asset_path: str, tensor, fps, content_type="gif", asset_rel_path: str = None
):
    try:
        import moviepy  # noqa: F401
    except ImportError:
        logger.warning(MOVIEPY_ERROR_MESSAGE)
        return UNKNOWN
    try:
        from moviepy import editor as mpy
    except ImportError:
        logger.warning(
            "moviepy is installed, but can't import moviepy.editor.",
            "Some packages could be missing [imageio, requests]",
        )
        return

    t, h, w, c = tensor.shape

    # encode sequence of images into gif string
    clip = mpy.ImageSequenceClip(list(tensor), fps=fps)

    check_or_create_path(asset_path, is_dir=False)

    try:  # older version of moviepy
        if content_type == "gif":
            clip.write_gif(asset_path, verbose=False, progress_bar=False)
        else:
            clip.write_videofile(asset_path, verbose=False, progress_bar=False)
    except TypeError:
        if content_type == "gif":
            clip.write_gif(asset_path, verbose=False)
        else:
            clip.write_videofile(asset_path, verbose=False)

    return V1EventVideo(
        height=h,
        width=w,
        colorspace=c,
        path=asset_rel_path or asset_path,
        content_type=content_type,
    )


def audio(asset_path: str, tensor, sample_rate=44100, asset_rel_path: str = None):
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    tensor = to_np(tensor)
    tensor = tensor.squeeze()
    if abs(tensor).max() > 1:
        print("warning: audio amplitude out of range, auto clipped.")
        tensor = tensor.clip(-1, 1)
    assert tensor.ndim == 1, "input tensor should be 1 dimensional."

    tensor_list = [int(32767.0 * x) for x in tensor]

    import struct
    import wave

    check_or_create_path(asset_path, is_dir=False)

    wave_write = wave.open(asset_path, "wb")
    wave_write.setnchannels(1)
    wave_write.setsampwidth(2)
    wave_write.setframerate(sample_rate)
    tensor_enc = b""
    for v in tensor_list:
        tensor_enc += struct.pack("<h", v)

    wave_write.writeframes(tensor_enc)
    wave_write.close()
    return V1EventAudio(
        sample_rate=sample_rate,
        num_channels=1,
        length_frames=len(tensor_list),
        path=asset_rel_path or asset_path,
        content_type="audio/wav",
    )


def roc_auc_curve(fpr, tpr, auc=None):
    return V1EventCurve(
        kind=V1EventCurveKind.ROC,
        x=fpr,
        y=tpr,
        annotation=str(auc) if auc else None,
    )


def sklearn_roc_auc_curve(y_preds, y_targets, pos_label=None):
    try:
        from sklearn.metrics import auc, roc_curve
    except ImportError:
        logger.warning(SKLEARN_ERROR_MESSAGE)

    try:
        y_true = y_targets.numpy()
    except AttributeError:
        y_true = y_targets
    try:
        y_pred = y_preds.numpy()
    except AttributeError:
        y_pred = y_preds
    fpr, tpr, _ = roc_curve(y_true, y_pred, pos_label=pos_label)
    auc_score = auc(fpr, tpr)
    return V1EventCurve(
        kind=V1EventCurveKind.ROC,
        x=fpr,
        y=tpr,
        annotation=str(auc_score),
    )


def pr_curve(precision, recall, average_precision=None):
    return V1EventCurve(
        kind=V1EventCurveKind.PR,
        x=precision,
        y=recall,
        annotation=str(average_precision) if average_precision else None,
    )


def sklearn_pr_curve(y_preds, y_targets, pos_label=None):
    try:
        from sklearn.metrics import average_precision_score, precision_recall_curve
    except ImportError:
        logger.warning(SKLEARN_ERROR_MESSAGE)

    try:
        y_true = y_targets.numpy()
    except AttributeError:
        y_true = y_targets
    try:
        y_pred = y_preds.numpy()
    except AttributeError:
        y_pred = y_preds

    precision, recall, _ = precision_recall_curve(y_true, y_pred, pos_label=pos_label)
    ap = average_precision_score(y_true, y_pred)
    return V1EventCurve(
        kind=V1EventCurveKind.PR,
        x=precision,
        y=recall,
        annotation=str(ap),
    )


def curve(x, y, annotation=None):
    return V1EventCurve(
        kind=V1EventCurveKind.CUSTOM,
        x=x,
        y=y,
        annotation=str(annotation) if annotation else None,
    )


def confusion_matrix(x, y, z):
    try:
        x_len = len(x)
        y_len = len(y)
        z_len = len(z)
        if x_len != y_len or x_len != z_len:
            raise ValueError(
                "Received invalid data for confusion matrix. "
                "All arrays must have the same structure: "
                "[len(x): {}, len(y): {}, len(z): {}]".format(
                    x_len,
                    y_len,
                    z_len,
                )
            )
        zi_len = [len(zi) for zi in z]
        if len(set(zi_len)) != 1 or zi_len[0] != z_len:
            raise ValueError(
                "Received invalid data for confusion matrix. "
                "Current structure: [len(x): {}, len(y): {}, len(z): {}]. "
                "The z array has different nested structures: {}".format(
                    x_len, y_len, z_len, zi_len
                )
            )
    except Exception as e:  # noqa
        raise ValueError(
            "Received invalid data for confusion matrix. Error {}".format(e)
        )
    return V1EventConfusionMatrix(
        x=x,
        y=y,
        z=z,
    )


def figure_to_image(figure, close=True):
    """Render matplotlib figure to numpy format.

    Returns:
        numpy.array: image in [CHW] order
    """
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)

    try:
        import matplotlib.backends.backend_agg as plt_backend_agg
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning(MATPLOTLIB_ERROR_MESSAGE)

    canvas = plt_backend_agg.FigureCanvasAgg(figure)
    canvas.draw()
    data = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
    w, h = figure.canvas.get_width_height()
    image_hwc = data.reshape([h, w, 4])[:, :, 0:3]
    image_chw = np.moveaxis(image_hwc, source=2, destination=0)
    if close:
        try:
            plt.close(figure.number)
        except Exception:  # noqa
            plt.close(figure)
    return image_chw


def figures_to_images(figures, close=True):
    """Render matplotlib figure to numpy format.

    Returns:
        numpy.array: image in [CHW] order
    """
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    images = [figure_to_image(figure, close=close) for figure in figures]
    return np.stack(images)


def ensure_matplotlib_figure(figure):
    """Extract the current figure from a matplotlib object or return the object if it's a figure.
    raises ValueError if the object can't be converted.
    """
    import matplotlib

    from matplotlib.figure import Figure

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
    if not figure.gca().has_data():
        raise ValueError(
            "You attempted to log an empty plot, "
            "pass a figure directly or ensure the global plot isn't closed."
        )
    return figure


def prepare_video(data):
    """
    Converts a 5D tensor [batchsize, time(frame), channel(color), height, width]
    into 4D tensor with dimension [time(frame), new_width, new_height, channel].
    A batch of images are spreaded to a grid, which forms a frame.
    e.g. Video with batchsize 16 will have a 4x4 grid.
    """
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    b, t, c, h, w = data.shape

    if data.dtype == np.uint8:
        data = np.float32(data) / 255.0

    def is_power2(num):
        return num != 0 and ((num & (num - 1)) == 0)

    # pad to nearest power of 2, all at once
    if not is_power2(data.shape[0]):
        len_addition = int(2 ** data.shape[0].bit_length() - data.shape[0])
        data = np.concatenate(
            (data, np.zeros(shape=(len_addition, t, c, h, w))), axis=0
        )

    n_rows = 2 ** ((b.bit_length() - 1) // 2)
    n_cols = data.shape[0] // n_rows

    data = np.reshape(data, newshape=(n_rows, n_cols, t, c, h, w))
    data = np.transpose(data, axes=(2, 0, 4, 1, 5, 3))
    return np.reshape(data, newshape=(t, n_rows * h, n_cols * w, c))


def make_grid(data, ncols=8):
    # I: N1HW or N3HW
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    assert isinstance(data, np.ndarray), "plugin error, should pass numpy array here"
    if data.shape[1] == 1:
        data = np.concatenate([data, data, data], 1)
    assert data.ndim == 4 and data.shape[1] == 3 or data.shape[1] == 4
    nimg = data.shape[0]
    H = data.shape[2]  # noqa
    W = data.shape[3]  # noqa
    ncols = min(nimg, ncols)
    nrows = int(np.ceil(float(nimg) / ncols))
    canvas = np.zeros((data.shape[1], H * nrows, W * ncols))
    i = 0
    for y in range(nrows):
        for x in range(ncols):
            if i >= nimg:
                break
            canvas[:, y * H : (y + 1) * H, x * W : (x + 1) * W] = data[i]  # noqa
            i = i + 1
    return canvas


def convert_to_HWC(tensor, input_format):  # noqa
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    assert len(set(input_format)) == len(
        input_format
    ), "You can not use the same dimension shordhand twice. \
        input_format: {}".format(
        input_format
    )
    assert len(tensor.shape) == len(
        input_format
    ), "size of input tensor and input format are different. \
        tensor shape: {}, input_format: {}".format(
        tensor.shape, input_format
    )
    input_format = input_format.upper()

    if len(input_format) == 4:
        index = [input_format.find(c) for c in "NCHW"]
        tensor_NCHW = tensor.transpose(index)  # noqa
        tensor_CHW = make_grid(tensor_NCHW)  # noqa
        return tensor_CHW.transpose(1, 2, 0)

    if len(input_format) == 3:
        index = [input_format.find(c) for c in "HWC"]
        tensor_HWC = tensor.transpose(index)  # noqa
        if tensor_HWC.shape[2] == 1:
            tensor_HWC = np.concatenate([tensor_HWC, tensor_HWC, tensor_HWC], 2)  # noqa
        return tensor_HWC

    if len(input_format) == 2:
        index = [input_format.find(c) for c in "HW"]
        tensor = tensor.transpose(index)
        tensor = np.stack([tensor, tensor, tensor], 2)
        return tensor


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
    except ImportError:
        logger.warning(PLOTLY_ERROR_MESSAGE)
        return UNKNOWN

    if module_type(figure, "matplotlib.figure.Figure"):
        figure = plotly.tools.mpl_to_plotly(figure)

    else:
        figure = plotly.tools.return_figure_from_figure_or_data(
            figure, validate_figure=True
        )
    return V1EventChart(kind=V1EventChartKind.PLOTLY, figure=figure)


def mpl_plotly_chart(figure) -> V1EventChart:
    try:
        import plotly.tools
    except ImportError:
        logger.warning(PLOTLY_ERROR_MESSAGE)
        return UNKNOWN

    try:
        import matplotlib

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

    # This code was taken from:
    # https://github.com/matplotlib/matplotlib/pull/16772/files#diff-506cc6d736a0593e8bb820981b2c12ae # noqa
    # Removed in https://github.com/matplotlib/matplotlib/pull/16772
    from matplotlib.spines import Spine

    def is_frame_like(self):
        """return True if directly on axes frame
        This is useful for determining if a spine is the edge of an
        old style MPL plot. If so, this function will return True.
        """
        self._ensure_position_is_set()
        position = self._position
        if isinstance(position, str):
            if position == "center":
                position = ("axes", 0.5)
            elif position == "zero":
                position = ("data", 0)
        if len(position) != 2:
            raise ValueError("position should be 2-tuple")
        position_type, amount = position
        if position_type == "outward" and amount == 0:
            return True
        else:
            return False

    Spine.is_frame_like = is_frame_like
    figure = plotly.tools.mpl_to_plotly(figure)
    return plotly_chart(figure=figure)


def metrics_dict_to_list(metrics: Dict) -> List:
    results = []
    for k, v in metrics.items():
        results.append(
            LoggedEventSpec(
                name=k,
                kind=V1ArtifactKind.METRIC,
                event=V1Event.make(metric=v),
            )
        )
    return results


def _model_to_str(model):
    filetype = "txt"
    if hasattr(model, "to_json"):
        model = model.model.to_json()
        filetype = "json"
    elif hasattr(model, "to_yaml"):
        model = model.to_yaml()
        filetype = "yaml"

    try:
        return str(model), filetype
    except Exception as e:
        logger.warning("Could not convert model to a string. Error: %s" % e)


def model_to_str(model):
    # Tensorflow Graph Definition
    if type(model).__name__ == "Graph":
        try:
            from google.protobuf import json_format

            graph_def = model.as_graph_def()
            model = json_format.MessageToJson(graph_def, sort_keys=True)
        except Exception as e:  # noqa
            logger.warning(
                "Could not convert Tensorflow graph to JSON %s", e, exc_info=True
            )

    return _model_to_str(model)
