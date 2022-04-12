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
from polyaxon.utils.np_utils import calculate_scale_factor, to_np
from polyaxon.utils.path_utils import check_or_create_path, copy_file_path
from traceml.events import V1EventVideo
from traceml.logger import logger
from traceml.processors.errors import MOVIEPY_ERROR_MESSAGE, NUMPY_ERROR_MESSAGE

try:
    import numpy as np
except ImportError:
    np = None


def video_path(
    from_path: str, asset_path: str, content_type=None, asset_rel_path: str = None
) -> V1EventVideo:
    copy_file_path(from_path, asset_path)
    return V1EventVideo(path=asset_rel_path or asset_path, content_type=content_type)


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
