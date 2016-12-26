# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import random

import numpy as np

import scipy.ndimage


def get_batch_shape(batch):
    batch_shape = batch[0].shape
    return batch_shape[0], batch_shape[1]


def apply_transform(x, transform_matrix, fill_mode='nearest', cval=0.):
    x = np.rollaxis(x, 2, 0)
    final_affine_matrix = transform_matrix[:2, :2]
    final_offset = transform_matrix[:2, 2]
    channel_images = [scipy.ndimage.interpolation.affine_transform(
        x_channel, final_affine_matrix, final_offset, order=0, mode=fill_mode, cval=cval)
                      for x_channel in x]
    x = np.stack(channel_images, axis=0)
    x = np.rollaxis(x, 0, 2 + 1)
    return x


def transform_matrix_offset_center(matrix, x, y):
    """Return transform matrix offset center.

    Used with `rotation`, `shear`, `zoom`.

    Args:
        matrix : `numpy array` Transform matrix.
        x : `int`.
        y : `int`.
    """
    o_x = float(x) / 2 + 0.5
    o_y = float(y) / 2 + 0.5
    offset_matrix = np.array([[1, 0, o_x], [0, 1, o_y], [0, 0, 1]])
    reset_matrix = np.array([[1, 0, -o_x], [0, 1, -o_y], [0, 0, 1]])
    transform_matrix = np.dot(np.dot(offset_matrix, matrix), reset_matrix)
    return transform_matrix


def crop(batch, crop_height, crop_width, is_random=True, padding=None):
    """Randomly or centrally crop an image according to `crop_height`, `crop_width`.
    An optional padding can be specified, for padding picture with 0s (To conserve original
    image shape).

    Args:
        batch:
        crop_height: `int`. The crop shape height.
        crop_width: `int`. The crop shape width.
        is_random : `boolean`. random crop or central crop.
        padding: `int`. If not None, the image is padded with 'padding' 0s.

    Examples:
    ```python
    >>> # Example: pictures of 32x32
    >>> # Random crop of 24x24 into a 32x32 picture => output 24x24
    >>> crop(batch, crop_height=24, crop_width=24)
    >>> # Random crop of 32x32 with image padding of 6 #
    >>> # (to conserve original image shape) => output 32x32
    >>> crop(batch, crop_height=32, crop_width=32, padding=6)
    ```
    """
    shape_w, shape_h = get_batch_shape(batch)
    if padding:
        shape_w, shape_h = shape_w + 2 * padding, shape_h + 2 * padding
    new_batch = []
    pad_width = ((padding, padding), (padding, padding), (0, 0))

    if is_random:
        h_offset = random.randint(0, shape_w - crop_height)
        w_offset = random.randint(0, shape_h - crop_width)
    else:  # central crop
        h_offset = int(np.floor((shape_w - crop_height) / 2.))
        w_offset = int(np.floor((shape_h - crop_width) / 2.))

    for i in range(len(batch)):
        new_i_batch = batch[i]
        if padding:
            new_i_batch = np.lib.pad(new_i_batch, pad_width=pad_width,
                                     mode='constant', constant_values=0)
        new_i_batch = new_i_batch[
                      h_offset:h_offset + crop_height, w_offset:w_offset + crop_width]
        new_batch.append(new_i_batch)
    return np.asarray(new_batch)


def flip(batch, axis=0, is_random=True):
    """Flip an image (left to right) `axis` 0 or (up and down) if `axis` 1.

    Args:
        batch:
        axis: `int`. 0 for horizontal, 1 for vertical
        is_random : `boolean`.
    """
    flip = True if not is_random else np.random.uniform(-1, 1) > 0
    flip_fct = np.fliplr if axis == 0 else np.flipud
    for i in range(len(batch)):
        if flip:
            batch[i] = flip_fct(batch[i])
    return batch


def shift(batch, width_pct=0.1, height_pct=0.1, is_random=True, fill_mode='nearest', cval=0.):
    """Shift an image.

    Args:
        batch:
        width_pct : `float`. Percentage of shift in axis x, usually -0.25 ~ 0.25.
        height_pct : `float`. Percentage of shift in axis y, usually -0.25 ~ 0.25.
        is_random : `boolean`.
        fill_mode : `string`.
            Method to fill missing pixel, option: ‘nearest’, ‘constant’, ‘reflect’ or ‘wrap’.
            - `scipy ndimage affine_transform <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.interpolation.affine_transform.html>`_
        cval : `float`. Value used for points outside the boundaries of the input if mode='constant'.
            - `scipy ndimage affine_transform <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.interpolation.affine_transform.html>`_
    """
    shape_w, shape_h = get_batch_shape(batch)

    if is_random:
        tx = np.random.uniform(-height_pct, height_pct) * shape_h
        ty = np.random.uniform(-width_pct, width_pct) * shape_w
    else:
        tx, ty = height_pct * shape_h, height_pct * shape_w

    translation_matrix = np.array([[1, 0, tx],
                                   [0, 1, ty],
                                   [0, 0, 1]])

    transform_matrix = translation_matrix  # no need to do offset
    new_batch = []
    for i in range(len(batch)):
        x = apply_transform(batch[i], transform_matrix, fill_mode, cval)
        new_batch.append(x)
    return np.asarray(new_batch)


def blur(batch, sigma_max=5., is_random=True):
    """Randomly blur an image by applying a gaussian filter with a random sigma (0., sigma_max).

    Args:
        batch:
        sigma_max: `float` or list of `float`. Standard deviation for Gaussian
            kernel. The standard deviations of the Gaussian filter are
            given for each axis as a sequence, or as a single number,
            in which case it is equal for all axes.
        is_random: `boolean`.
    """
    blur = True if not is_random else np.random.uniform(-1, 1) > 0
    for i in range(len(batch)):
        if blur:
            # Random sigma
            sigma = random.uniform(0., sigma_max)
            batch[i] = scipy.ndimage.filters.gaussian_filter(batch[i], sigma)
    return np.asarray(batch)


def zoom(batch, zoom_range=(0.9, 1.1), is_random=True, fill_mode='nearest', cval=0.):
    """Zoom in and out of images, randomly or non-randomly.

    Args:
        batch:
        zoom_range: `list` or `tuple`.
            - If is_random=False, (h, w) are the fixed zoom factor for row and column axies,
              factor small than one is zoom in.
            - If is_random=True, (min zoom out, max zoom out) for x and y with different
              random zoom in/out factor.
            e.g (0.5, 1) zoom in 1~2 times.
        is_random: `boolean`.
        fill_mode: `string`.
            Method to fill missing pixel, option: ‘nearest’, ‘constant’, ‘reflect’ or ‘wrap’.
        cval: `float`.  Used for points outside the boundaries of the input if mode='constant'.
    """
    if len(zoom_range) != 2:
        raise Exception('zoom_range should be a tuple or list of two floats. '
                        'Received arg: ', zoom_range)
    if is_random:
        if zoom_range[0] == 1 and zoom_range[1] == 1:
            zx, zy = 1, 1
            print(" random_zoom : not zoom in/out")
        else:
            zx, zy = np.random.uniform(zoom_range[0], zoom_range[1], 2)
    else:
        zx, zy = zoom_range
    zoom_matrix = np.array([[zx, 0, 0],
                            [0, zy, 0],
                            [0, 0, 1]])

    shape_w, shape_h = get_batch_shape(batch)
    transform_matrix = transform_matrix_offset_center(zoom_matrix, shape_h, shape_w)
    new_batch = []
    for i in range(len(batch)):
        x = apply_transform(batch[i], transform_matrix, fill_mode, cval)
        new_batch.append(x)
    return np.asarray(new_batch)


def add_random_90degrees_rotation(batch, rotations=(0, 1, 2, 3)):
    """Rotate by 90 degrees.

    Args:
        batch:
        rotations: `tuple`. Allowed 90 degrees rotations.
    """
    for i in range(len(batch)):
        num_rotations = random.choice(rotations)
        batch[i] = np.rot90(batch[i], num_rotations)

    return np.asarray(batch)


def add_random_rotation(batch, max_angle=20., is_random=True):
    """Rotate an image by a random angle (-max_angle, max_angle).

    Args:
        batch:
        max_angle: `float`. The maximum rotation angle.
        is_random: `boolean`.
    """
    rotate = True if not is_random else np.random.uniform(-1, 1) > 0
    for i in range(len(batch)):
        if rotate:
            # Random angle
            angle = random.uniform(-max_angle, max_angle)
            batch[i] = scipy.ndimage.interpolation.rotate(batch[i], angle, reshape=False)
    return np.asarray(batch)


def add_drop(batch, drop=0.5):
    """Randomly set some pixels to zero by a given keeping probability.

    Args:
        batch: batch of `numpy array` (An image with dims of [row, col, channel] or [row, col]).
        drop: `float` (0, 1), The drop probability, higher => more values will be set to zero.
    """
    batch_shape = batch[0].shape

    def drop_color(x):
        mask = np.random.binomial(n=1, p=1 - drop, size=batch_shape[:-1])
        for i in range(3):
            x[:, :, i] = np.multiply(x[:, :, i], mask)
        return x

    def drop_gray(x):
        return np.multiply(x, np.random.binomial(n=1, p=1 - drop, size=batch_shape))

    if len(batch_shape) == 3:
        if batch_shape[-1] == 3:  # color
            drop_fct = drop_color
        elif batch_shape[-1] == 1:  # greyscale image
            drop_fct = drop_gray
        else:
            raise Exception('Unsupported shape {}'.format(batch_shape))
    elif len(batch_shape) == 2 or 1:  # greyscale matrix (image) or vector
        drop_fct = drop_gray
    else:
        raise Exception('Unsupported shape {}'.format(batch_shape))

    new_batch = []
    for i in range(len(batch)):
        new_batch.append(drop_fct(new_batch[i]))
    return np.asarray(new_batch)
