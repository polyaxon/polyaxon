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
import numpy as np
import os
import pytest
import tempfile

from bokeh.plotting import figure
from PIL import Image
from plotly import figure_factory

from polyaxon.polyboard.processors.events_processors import (
    audio,
    bokeh_chart,
    convert_to_HWC,
    histogram,
    image,
    image_boxes,
    plotly_chart,
    prepare_video,
    video,
)
from tests.utils import BaseTestCase, tensor_np


@pytest.mark.tracking_mark
class TestEventValues(BaseTestCase):
    def setUp(self):
        self.run_path = tempfile.mkdtemp()
        self.asset_path = self.run_path + "/asset"

    def test_uint8_image(self):
        """Tests that uint8 image (pixel values in [0, 255]) is not changed"""
        assert os.path.exists(self.asset_path) is False
        event = image(
            asset_path=self.asset_path,
            data=tensor_np(shape=(3, 32, 32), dtype=np.uint8),
        )
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_float32_image(self):
        """Tests that float32 image (pixel values in [0, 1]) are scaled correctly to [0, 255]"""
        assert os.path.exists(self.asset_path) is False
        event = image(asset_path=self.asset_path, data=tensor_np(shape=(3, 32, 32)))
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_float_1_converts_to_uint8_255(self):
        assert os.path.exists(self.asset_path) is False
        green_uint8 = np.array([[[0, 255, 0]]], dtype="uint8")
        green_float32 = np.array([[[0, 1, 0]]], dtype="float32")

        a = image(asset_path=self.run_path + "/asset1", data=green_uint8)
        b = image(asset_path=self.run_path + "/asset2", data=green_float32)
        self.assertEqual(
            Image.open(io.BytesIO(open(a.path, "br").read())),
            Image.open(io.BytesIO(open(b.path, "br").read())),
        )

    def test_list_input(self):
        with pytest.raises(Exception):
            histogram("dummy", [1, 3, 4, 5, 6], "tensorflow")

    def test_empty_input(self):
        print("expect error here:")
        with pytest.raises(Exception):
            histogram("dummy", np.ndarray(0), "tensorflow")

    def test_image_with_boxes(self):
        event = image_boxes(
            asset_path=self.asset_path,
            tensor_image=tensor_np(shape=(3, 32, 32)),
            tensor_boxes=np.array([[10, 10, 40, 40]]),
        )
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_image_with_one_channel(self):
        event = image(
            asset_path=self.asset_path,
            data=tensor_np(shape=(1, 8, 8)),
            dataformats="CHW",
        )
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_image_with_four_channel(self):
        event = image(
            asset_path=self.asset_path,
            data=tensor_np(shape=(4, 8, 8)),
            dataformats="CHW",
        )
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_image_with_one_channel_batched(self):
        event = image(
            asset_path=self.asset_path,
            data=tensor_np(shape=(2, 1, 8, 8)),
            dataformats="NCHW",
        )
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_image_with_3_channel_batched(self):
        event = image(
            asset_path=self.asset_path,
            data=tensor_np(shape=(2, 3, 8, 8)),
            dataformats="NCHW",
        )
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_image_with_four_channel_batched(self):
        event = image(
            asset_path=self.asset_path,
            data=tensor_np(shape=(2, 4, 8, 8)),
            dataformats="NCHW",
        )
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_image_without_channel(self):
        event = image(
            asset_path=self.asset_path, data=tensor_np(shape=(8, 8)), dataformats="HW"
        )
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_video(self):
        asset_path = self.asset_path + ".gif"
        event = video(asset_path=asset_path, tensor=tensor_np(shape=(4, 3, 1, 8, 8)))
        assert event.path == asset_path
        assert os.path.exists(asset_path) is True
        event = video(
            asset_path=asset_path, tensor=tensor_np(shape=(16, 48, 1, 28, 28))
        )
        assert event.path == asset_path
        assert os.path.exists(asset_path) is True
        event = video(asset_path=asset_path, tensor=tensor_np(shape=(20, 7, 1, 8, 8)))
        assert event.path == asset_path
        assert os.path.exists(asset_path) is True

    def test_audio(self):
        event = audio(asset_path=self.asset_path, tensor=tensor_np(shape=(42,)))
        assert event.path == self.asset_path
        assert os.path.exists(self.asset_path) is True

    def test_histogram_auto(self):
        event = histogram(values=tensor_np(shape=(1024,)), bins="auto", max_bins=5)
        assert event.values is not None
        assert event.counts is not None

    def test_histogram(self):
        event = histogram(values=tensor_np(shape=(1024,)), bins="fd", max_bins=5)
        assert event.values is not None
        assert event.counts is not None

    def test_histogram_doane(self):
        event = histogram(tensor_np(shape=(1024,)), bins="doane", max_bins=5)
        assert event.values is not None
        assert event.counts is not None

    def test_to_HWC(self):  # noqa
        np.random.seed(1)
        test_image = np.random.randint(0, 256, size=(3, 32, 32), dtype=np.uint8)
        converted = convert_to_HWC(test_image, "chw")
        assert converted.shape == (32, 32, 3)
        test_image = np.random.randint(0, 256, size=(16, 3, 32, 32), dtype=np.uint8)
        converted = convert_to_HWC(test_image, "nchw")
        assert converted.shape == (64, 256, 3)
        test_image = np.random.randint(0, 256, size=(32, 32), dtype=np.uint8)
        converted = convert_to_HWC(test_image, "hw")
        assert converted.shape == (32, 32, 3)

    def test_prepare_video(self):
        # at each timestep the sum over all other dimensions of the video should stay the same
        np.random.seed(1)
        video_before = np.random.random((4, 10, 3, 20, 20))
        video_after = prepare_video(np.copy(video_before))
        video_before = np.swapaxes(video_before, 0, 1)
        video_before = np.reshape(video_before, newshape=(10, -1))
        video_after = np.reshape(video_after, newshape=(10, -1))
        np.testing.assert_array_almost_equal(
            np.sum(video_before, axis=1), np.sum(video_after, axis=1)
        )

    def test_bokeh_chart(self):
        # prepare some data
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 2, 4, 5]

        # create a new plot with a title and axis labels
        p = figure(title="simple line example", x_axis_label="x", y_axis_label="y")

        # add a line renderer with legend and line thickness
        p.line(x, y, line_width=2)

        # show the results
        event = bokeh_chart(p)
        assert isinstance(event.figure, dict)

    def test_plotly_chart(self):
        x1 = np.random.randn(200) - 2
        x2 = np.random.randn(200)
        x3 = np.random.randn(200) + 2
        hist_data = [x1, x2, x3]
        group_labels = ["Group 1", "Group 2", "Group 3"]
        p = figure_factory.create_distplot(
            hist_data, group_labels, bin_size=[0.1, 0.25, 0.5]
        )

        # show the results
        event = plotly_chart(p)
        assert isinstance(event.figure, dict)
