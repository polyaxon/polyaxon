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
import io

from polyaxon.constants.globals import UNKNOWN
from polyaxon.utils.np_utils import calculate_scale_factor, to_np
from polyaxon.utils.path_utils import check_or_create_path, copy_file_path
from traceml.events import V1EventImage
from traceml.logger import logger
from traceml.processors.errors import (
    MATPLOTLIB_ERROR_MESSAGE,
    NUMPY_ERROR_MESSAGE,
    PIL_ERROR_MESSAGE,
)

try:
    import numpy as np
except ImportError:
    np = None


def image_path(
    from_path: str, asset_path: str, asset_rel_path: str = None
) -> V1EventImage:
    copy_file_path(from_path, asset_path)
    return V1EventImage(path=asset_rel_path or asset_path)


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


def figure_to_image(figure, close: bool = True):
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
    try:
        import matplotlib

        from matplotlib.figure import Figure
    except ImportError:
        logger.warning(MATPLOTLIB_ERROR_MESSAGE)

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
