# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from six.moves import xrange

import numpy as np
import tensorflow as tf

from tensorflow.contrib.slim.python.slim.data import tfexample_decoder
from tensorflow.core.example import example_pb2
from tensorflow.core.example import feature_pb2
from tensorflow.python.framework import constant_op
from tensorflow.python.framework import dtypes
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import image_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import parsing_ops
from tensorflow.python.platform import test

from polyaxon.processing.data_decoders import TFExampleDecoder


class TFExampleDecoderTest(test.TestCase):
    def _encode_float_feature(self, ndarray):
        return feature_pb2.Feature(
            float_list=feature_pb2.FloatList(value=ndarray.flatten().tolist()))

    def _encode_int64_feature(self, ndarray):
        return feature_pb2.Feature(
            int64_list=feature_pb2.Int64List(value=ndarray.flatten().tolist()))

    def _encode_bytes_feature(self, tf_encoded):
        with self.test_session():
            encoded = tf_encoded.eval()

        def bytes_list(value):
            return feature_pb2.BytesList(value=[value])

        return feature_pb2.Feature(bytes_list=bytes_list(encoded))

    def _bytes_feature(self, ndarray):
        values = ndarray.flatten().tolist()
        for i in xrange(len(values)):
            values[i] = values[i].encode('utf-8')
        return feature_pb2.Feature(bytes_list=feature_pb2.BytesList(value=values))

    def _string_feature(self, value):
        value = value.encode('utf-8')
        return feature_pb2.Feature(bytes_list=feature_pb2.BytesList(value=[value]))

    def _encode(self, image, image_format):
        assert image_format in ['jpeg', 'JPEG', 'png', 'PNG', 'raw', 'RAW']
        if image_format in ['jpeg', 'JPEG']:
            tf_image = constant_op.constant(image, dtype=dtypes.uint8)
            return image_ops.encode_jpeg(tf_image)
        if image_format in ['png', 'PNG']:
            tf_image = constant_op.constant(image, dtype=dtypes.uint8)
            return image_ops.encode_png(tf_image)
        if image_format in ['raw', 'RAW']:
            return constant_op.constant(image.tostring(), dtype=dtypes.string)

    def generate_image(self, image_format, image_shape):
        """Generates an image and an example containing the encoded image.

        Args:
            image_format: the encoding format of the image.
            image_shape: the shape of the image to generate.
    
        Returns:
            image: the generated image.
            example: a TF-example with a feature key 'image/encoded' set to the
                serialized image and a feature key 'image/format' set to the image
                encoding format ['jpeg', 'JPEG', 'png', 'PNG', 'raw'].
        """
        num_pixels = image_shape[0] * image_shape[1] * image_shape[2]
        image = np.linspace(0, num_pixels - 1, num=num_pixels).reshape(image_shape).astype(np.uint8)
        tf_encoded = self._encode(image, image_format)
        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'image/encoded': self._encode_bytes_feature(tf_encoded),
            'image/format': self._string_feature(image_format)
        }))

        return image, example.SerializeToString()

    def decode_example(self, serialized_example, item_handler, image_format):
        """Decodes the given serialized example with the specified item handler.

        Args:
            serialized_example: a serialized TF example string.
            item_handler: the item handler used to decode the image.
            image_format: the image format being decoded.

        Returns:
            the decoded image found in the serialized Example.
        """
        serialized_example = array_ops.reshape(serialized_example, shape=[])
        decoder = TFExampleDecoder(
            keys_to_features={
                'image/encoded': tf.FixedLenFeature((), dtypes.string, default_value=''),
                'image/format': tf.FixedLenFeature((), dtypes.string, default_value=image_format),
            },
            items_to_handlers={'image': item_handler})
        [tf_image] = decoder.decode(serialized_example, ['image'])
        return tf_image

    def run_decode_example(self, serialized_example, item_handler, image_format):
        tf_image = self.decode_example(serialized_example, item_handler, image_format)

        with self.test_session():
            decoded_image = tf_image.eval()

            # We need to recast them here to avoid some issues with uint8.
            return decoded_image.astype(np.float32)

    def test_decode_example_with_jpeg_encoding(self):
        image_shape = (2, 3, 3)
        image, serialized_example = self.generate_image(image_format='jpeg',
                                                        image_shape=image_shape)

        decoded_image = self.run_decode_example(
            serialized_example, tfexample_decoder.Image(), image_format='jpeg')

        # Need to use a tolerance of 1 because of noise in the jpeg encode/decode
        self.assertAllClose(image, decoded_image, atol=1.001)

    def test_decode_example_with_JPEG_encoding(self):
        test_image_channels = [1, 3]
        for channels in test_image_channels:
            image_shape = (2, 3, channels)
            image, serialized_example = self.generate_image(
                image_format='JPEG', image_shape=image_shape)

            decoded_image = self.run_decode_example(
                serialized_example,
                tfexample_decoder.Image(channels=channels),
                image_format='JPEG')

            # Need to use a tolerance of 1 because of noise in the jpeg encode/decode
            self.assertAllClose(image, decoded_image, atol=1.001)

    def test_decode_example_with_no_shape_info(self):
        test_image_channels = [1, 3]
        for channels in test_image_channels:
            image_shape = (2, 3, channels)
            _, serialized_example = self.generate_image(image_format='jpeg',
                                                        image_shape=image_shape)

            tf_decoded_image = self.decode_example(
                serialized_example,
                tfexample_decoder.Image(shape=None, channels=channels),
                image_format='jpeg')
            self.assertEqual(tf_decoded_image.get_shape().ndims, 3)

    def test_decode_example_with_png_encoding(self):
        test_image_channels = [1, 3, 4]
        for channels in test_image_channels:
            image_shape = (2, 3, channels)
            image, serialized_example = self.generate_image(
                image_format='png', image_shape=image_shape)

            decoded_image = self.run_decode_example(
                serialized_example,
                tfexample_decoder.Image(channels=channels),
                image_format='png')

            self.assertAllClose(image, decoded_image, atol=0)

    def test_decode_example_with_PNG_encoding(self):
        test_image_channels = [1, 3, 4]
        for channels in test_image_channels:
            image_shape = (2, 3, channels)
            image, serialized_example = self.generate_image(image_format='PNG',
                                                            image_shape=image_shape)

            decoded_image = self.run_decode_example(
                serialized_example,
                tfexample_decoder.Image(channels=channels),
                image_format='PNG')

            self.assertAllClose(image, decoded_image, atol=0)

    def test_decode_example_with_raw_encoding(self):
        image_shape = (2, 3, 3)
        image, serialized_example = self.generate_image(image_format='raw', image_shape=image_shape)

        decoded_image = self.run_decode_example(
            serialized_example,
            tfexample_decoder.Image(shape=image_shape),
            image_format='raw')

        self.assertAllClose(image, decoded_image, atol=0)

    def test_decode_example_with_RAW_encoding(self):
        image_shape = (2, 3, 3)
        image, serialized_example = self.generate_image(image_format='RAW', image_shape=image_shape)

        decoded_image = self.run_decode_example(
            serialized_example,
            tfexample_decoder.Image(shape=image_shape),
            image_format='RAW')

        self.assertAllClose(image, decoded_image, atol=0)

    def test_decode_example_with_jpeg_encoding_at_16Bit_causes_error(self):
        image_shape = (2, 3, 3)
        unused_image, serialized_example = self.generate_image(
            image_format='jpeg', image_shape=image_shape)
        with self.assertRaises((TypeError, ValueError)):
            self.run_decode_example(serialized_example,
                                    tfexample_decoder.Image(dtype=dtypes.uint16),
                                    image_format='jpeg')

    def test_decode_example_with_string_tensor(self):
        tensor_shape = (2, 3, 1)
        np_array = np.array([[['ab'], ['cd'], ['ef']], [['ghi'], ['jkl'], ['mnop']]])

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'labels': self._bytes_feature(np_array),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'labels': parsing_ops.FixedLenFeature(
                    tensor_shape, dtypes.string,
                    default_value=constant_op.constant('', shape=tensor_shape, dtype=dtypes.string))
            }
            items_to_handlers = {'labels': tfexample_decoder.Tensor('labels')}
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_labels] = decoder.decode(serialized_example, ['labels'])
            labels = tf_labels.eval()

            labels = labels.astype(np_array.dtype)
            self.assertTrue(np.array_equal(np_array, labels))

    def test_decode_example_with_float_tensor(self):
        np_array = np.random.rand(2, 3, 1).astype('f')

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'array': self._encode_float_feature(np_array),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'array': parsing_ops.FixedLenFeature(np_array.shape, dtypes.float32)
            }
            items_to_handlers = {'array': tfexample_decoder.Tensor('array'), }
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_array] = decoder.decode(serialized_example, ['array'])
            self.assertAllEqual(tf_array.eval(), np_array)

    def test_decode_example_with_iInt64_tensor(self):
        np_array = np.random.randint(1, 10, size=(2, 3, 1))

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'array': self._encode_int64_feature(np_array),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'array': parsing_ops.FixedLenFeature(np_array.shape, dtypes.int64)
            }
            items_to_handlers = {'array': tfexample_decoder.Tensor('array'), }
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_array] = decoder.decode(serialized_example, ['array'])
            self.assertAllEqual(tf_array.eval(), np_array)

    def test_decode_example_with_var_len_tensor(self):
        np_array = np.array([[[1], [2], [3]], [[4], [5], [6]]])

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'labels': self._encode_int64_feature(np_array),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'labels': parsing_ops.VarLenFeature(dtype=dtypes.int64),
            }
            items_to_handlers = {'labels': tfexample_decoder.Tensor('labels'), }
            decoder = TFExampleDecoder(keys_to_features,
                                       items_to_handlers)
            [tf_labels] = decoder.decode(serialized_example, ['labels'])
            labels = tf_labels.eval()
            self.assertAllEqual(labels, np_array.flatten())

    def test_decode_example_with_fix_len_tensor_with_shape(self):
        np_array = np.array([[1, 2, 3], [4, 5, 6]])

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'labels': self._encode_int64_feature(np_array),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'labels': parsing_ops.FixedLenFeature(np_array.shape, dtype=dtypes.int64),
            }
            items_to_handlers = {
                'labels': tfexample_decoder.Tensor('labels', shape=np_array.shape),
            }
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_labels] = decoder.decode(serialized_example, ['labels'])
            labels = tf_labels.eval()
            self.assertAllEqual(labels, np_array)

    def test_decode_example_with_var_len_tensor_to_dense(self):
        np_array = np.array([[1, 2, 3], [4, 5, 6]])
        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'labels': self._encode_int64_feature(np_array),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'labels': parsing_ops.VarLenFeature(dtype=dtypes.int64),
            }
            items_to_handlers = {
                'labels': tfexample_decoder.Tensor(
                    'labels', shape=np_array.shape),
            }
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_labels] = decoder.decode(serialized_example, ['labels'])
            labels = tf_labels.eval()
            self.assertAllEqual(labels, np_array)

    def test_decode_example_shape_key_tensor(self):
        np_image = np.random.rand(2, 3, 1).astype('f')
        np_labels = np.array([[[1], [2], [3]], [[4], [5], [6]]])

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'image': self._encode_float_feature(np_image),
            'image/shape': self._encode_int64_feature(np.array(np_image.shape)),
            'labels': self._encode_int64_feature(np_labels),
            'labels/shape': self._encode_int64_feature(np.array(np_labels.shape)),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'image': parsing_ops.VarLenFeature(dtype=dtypes.float32),
                'image/shape': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'labels': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'labels/shape': parsing_ops.VarLenFeature(dtype=dtypes.int64),
            }
            items_to_handlers = {
                'image':
                    tfexample_decoder.Tensor('image', shape_keys='image/shape'),
                'labels':
                    tfexample_decoder.Tensor('labels', shape_keys='labels/shape'),
            }
            decoder = TFExampleDecoder(keys_to_features,
                                       items_to_handlers)
            [tf_image, tf_labels] = decoder.decode(serialized_example,
                                                   ['image', 'labels'])
            self.assertAllEqual(tf_image.eval(), np_image)
            self.assertAllEqual(tf_labels.eval(), np_labels)

    def test_decode_example_multi_shape_key_tensor(self):
        np_image = np.random.rand(2, 3, 1).astype('f')
        np_labels = np.array([[[1], [2], [3]], [[4], [5], [6]]])
        height, width, depth = np_labels.shape

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'image': self._encode_float_feature(np_image),
            'image/shape': self._encode_int64_feature(np.array(np_image.shape)),
            'labels': self._encode_int64_feature(np_labels),
            'labels/height': self._encode_int64_feature(np.array([height])),
            'labels/width': self._encode_int64_feature(np.array([width])),
            'labels/depth': self._encode_int64_feature(np.array([depth])),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'image': parsing_ops.VarLenFeature(dtype=dtypes.float32),
                'image/shape': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'labels': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'labels/height': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'labels/width': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'labels/depth': parsing_ops.VarLenFeature(dtype=dtypes.int64),
            }
            items_to_handlers = {
                'image':
                    tfexample_decoder.Tensor('image', shape_keys='image/shape'),
                'labels':
                    tfexample_decoder.Tensor(
                        'labels',
                        shape_keys=['labels/height', 'labels/width', 'labels/depth']),
            }
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_image, tf_labels] = decoder.decode(serialized_example, ['image', 'labels'])
            self.assertAllEqual(tf_image.eval(), np_image)
            self.assertAllEqual(tf_labels.eval(), np_labels)

    def test_decode_example_with_sparse_tensor(self):
        np_indices = np.array([[1], [2], [5]])
        np_values = np.array([0.1, 0.2, 0.6]).astype('f')
        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'indices': self._encode_int64_feature(np_indices),
            'values': self._encode_float_feature(np_values),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'indices': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'values': parsing_ops.VarLenFeature(dtype=dtypes.float32),
            }
            items_to_handlers = {'labels': tfexample_decoder.SparseTensor()}
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_labels] = decoder.decode(serialized_example, ['labels'])
            labels = tf_labels.eval()
            self.assertAllEqual(labels.indices, np_indices)
            self.assertAllEqual(labels.values, np_values)
            self.assertAllEqual(labels.dense_shape, np_values.shape)

    def test_decode_example_with_sparse_tensor_with_key_shape(self):
        np_indices = np.array([[1], [2], [5]])
        np_values = np.array([0.1, 0.2, 0.6]).astype('f')
        np_shape = np.array([6])
        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'indices': self._encode_int64_feature(np_indices),
            'values': self._encode_float_feature(np_values),
            'shape': self._encode_int64_feature(np_shape),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'indices': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'values': parsing_ops.VarLenFeature(dtype=dtypes.float32),
                'shape': parsing_ops.VarLenFeature(dtype=dtypes.int64),
            }
            items_to_handlers = {
                'labels': tfexample_decoder.SparseTensor(shape_key='shape'),
            }
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_labels] = decoder.decode(serialized_example, ['labels'])
            labels = tf_labels.eval()
            self.assertAllEqual(labels.indices, np_indices)
            self.assertAllEqual(labels.values, np_values)
            self.assertAllEqual(labels.dense_shape, np_shape)

    def test_decode_example_with_sparse_tensor_with_given_shape(self):
        np_indices = np.array([[1], [2], [5]])
        np_values = np.array([0.1, 0.2, 0.6]).astype('f')
        np_shape = np.array([6])
        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'indices': self._encode_int64_feature(np_indices),
            'values': self._encode_float_feature(np_values),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'indices': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'values': parsing_ops.VarLenFeature(dtype=dtypes.float32),
            }
            items_to_handlers = {
                'labels': tfexample_decoder.SparseTensor(shape=np_shape),
            }
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_labels] = decoder.decode(serialized_example, ['labels'])
            labels = tf_labels.eval()
            self.assertAllEqual(labels.indices, np_indices)
            self.assertAllEqual(labels.values, np_values)
            self.assertAllEqual(labels.dense_shape, np_shape)

    def test_decode_example_with_sparse_tensor_to_dense(self):
        np_indices = np.array([1, 2, 5])
        np_values = np.array([0.1, 0.2, 0.6]).astype('f')
        np_shape = np.array([6])
        np_dense = np.array([0.0, 0.1, 0.2, 0.0, 0.0, 0.6]).astype('f')
        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'indices': self._encode_int64_feature(np_indices),
            'values': self._encode_float_feature(np_values),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])
            keys_to_features = {
                'indices': parsing_ops.VarLenFeature(dtype=dtypes.int64),
                'values': parsing_ops.VarLenFeature(dtype=dtypes.float32),
            }
            items_to_handlers = {
                'labels': tfexample_decoder.SparseTensor(shape=np_shape, densify=True),
            }
            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_labels] = decoder.decode(serialized_example, ['labels'])
            labels = tf_labels.eval()
            self.assertAllClose(labels, np_dense)

    def test_decode_example_with_tensor(self):
        tensor_shape = (2, 3, 1)
        np_array = np.random.rand(2, 3, 1)

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'image/depth_map': self._encode_float_feature(np_array),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])

            keys_to_features = {
                'image/depth_map':
                    parsing_ops.FixedLenFeature(
                        tensor_shape, dtypes.float32,
                        default_value=array_ops.zeros(tensor_shape))
            }

            items_to_handlers = {'depth': tfexample_decoder.Tensor('image/depth_map')}

            decoder = TFExampleDecoder(keys_to_features,
                                       items_to_handlers)
            [tf_depth] = decoder.decode(serialized_example, ['depth'])
            depth = tf_depth.eval()

        self.assertAllClose(np_array, depth)

    def test_decode_example_with_item_handler_callback(self):
        np.random.seed(0)
        tensor_shape = (2, 3, 1)
        np_array = np.random.rand(2, 3, 1)

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'image/depth_map': self._encode_float_feature(np_array),
        }))

        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])

            keys_to_features = {
                'image/depth_map':
                    parsing_ops.FixedLenFeature(
                        tensor_shape,
                        dtypes.float32,
                        default_value=array_ops.zeros(tensor_shape))
            }

            def handle_depth(keys_to_tensors):
                depth = list(keys_to_tensors.values())[0]
                depth += 1
                return depth

            items_to_handlers = {
                'depth': tfexample_decoder.ItemHandlerCallback('image/depth_map', handle_depth)
            }

            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_depth] = decoder.decode(serialized_example, ['depth'])
            depth = tf_depth.eval()

        self.assertAllClose(np_array, depth - 1)

    def test_decode_image_with_item_handler_callback(self):
        image_shape = (2, 3, 3)
        for image_encoding in ['jpeg', 'png']:
            image, serialized_example = self.generate_image(
                image_format=image_encoding, image_shape=image_shape)

            with self.test_session():

                def conditional_decoding(keys_to_tensors):
                    """See base class."""
                    image_buffer = keys_to_tensors['image/encoded']
                    image_format = keys_to_tensors['image/format']

                    def decode_png():
                        return image_ops.decode_png(image_buffer, 3)

                    def decode_jpg():
                        return image_ops.decode_jpeg(image_buffer, 3)

                    image = control_flow_ops.case(
                        {math_ops.equal(image_format, 'png'): decode_png},
                        default=decode_jpg,
                        exclusive=True)
                    image = array_ops.reshape(image, image_shape)
                    return image

                keys_to_features = {
                    'image/encoded': parsing_ops.FixedLenFeature(
                        (), dtypes.string, default_value=''),
                    'image/format': parsing_ops.FixedLenFeature(
                        (), dtypes.string, default_value='jpeg')
                }

                items_to_handlers = {
                    'image': tfexample_decoder.ItemHandlerCallback(
                        ['image/encoded', 'image/format'], conditional_decoding)
                }

                decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
                [tf_image] = decoder.decode(serialized_example, ['image'])
                decoded_image = tf_image.eval()
                if image_encoding == 'jpeg':
                    # For jenkins:
                    image = image.astype(np.float32)
                    decoded_image = decoded_image.astype(np.float32)
                    self.assertAllClose(image, decoded_image, rtol=.5, atol=1.001)
                else:
                    self.assertAllClose(image, decoded_image, atol=0)

    def test_decode_example_with_bounding_box(self):
        num_bboxes = 10
        np_ymin = np.random.rand(num_bboxes, 1)
        np_xmin = np.random.rand(num_bboxes, 1)
        np_ymax = np.random.rand(num_bboxes, 1)
        np_xmax = np.random.rand(num_bboxes, 1)
        np_bboxes = np.hstack([np_ymin, np_xmin, np_ymax, np_xmax])

        example = example_pb2.Example(features=feature_pb2.Features(feature={
            'image/object/bbox/ymin': self._encode_float_feature(np_ymin),
            'image/object/bbox/xmin': self._encode_float_feature(np_xmin),
            'image/object/bbox/ymax': self._encode_float_feature(np_ymax),
            'image/object/bbox/xmax': self._encode_float_feature(np_xmax),
        }))
        serialized_example = example.SerializeToString()

        with self.test_session():
            serialized_example = array_ops.reshape(serialized_example, shape=[])

            keys_to_features = {
                'image/object/bbox/ymin': parsing_ops.VarLenFeature(dtypes.float32),
                'image/object/bbox/xmin': parsing_ops.VarLenFeature(dtypes.float32),
                'image/object/bbox/ymax': parsing_ops.VarLenFeature(dtypes.float32),
                'image/object/bbox/xmax': parsing_ops.VarLenFeature(dtypes.float32),
            }

            items_to_handlers = {
                'object/bbox': tfexample_decoder.BoundingBox(['ymin', 'xmin', 'ymax', 'xmax'],
                                                             'image/object/bbox/'),
            }

            decoder = TFExampleDecoder(keys_to_features, items_to_handlers)
            [tf_bboxes] = decoder.decode(serialized_example, ['object/bbox'])
            bboxes = tf_bboxes.eval()

        self.assertAllClose(np_bboxes, bboxes)
