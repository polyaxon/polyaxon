# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import mock

from polyaxon_dockerizer.builder import DockerBuilder, build, build_and_push
from polyaxon_dockerizer.exceptions import BuildException
from rhea.specs import UriSpec
from urllib3.exceptions import ReadTimeoutError


class TestDockerBuilder(TestCase):
    @staticmethod
    def touch(path):
        with open(path, 'w') as f:
            f.write('test')

    def test_tagged_image(self):
        builder = DockerBuilder(build_context='.', image_name='image', image_tag='tag')
        assert builder.get_tagged_image() == 'image:tag'

    @mock.patch('docker.APIClient.images')
    def test_check_image(self, check_image):
        builder = DockerBuilder(build_context='.', image_name='image', image_tag='tag')
        builder.check_image()
        assert check_image.call_count == 1
        assert check_image.call_args[0] == ('image:tag',)

    def test_validate_registries(self):
        with self.assertRaises(BuildException):
            DockerBuilder(build_context='.',
                          image_name='image',
                          image_tag='tag',
                          registries='foo')

        with self.assertRaises(BuildException):
            DockerBuilder(build_context='.',
                          image_name='image',
                          image_tag='tag',
                          registries=['foo', UriSpec('user', 'pwd', 'host')])

        builder = DockerBuilder(build_context='.',
                                image_name='image',
                                image_tag='tag',
                                registries=[UriSpec('user', 'pwd', 'host')])

        assert builder.registries is not None

    @mock.patch('docker.APIClient.login')
    def test_login_registries(self, login_mock):
        builder = DockerBuilder(build_context='.',
                                image_name='image',
                                image_tag='tag',
                                registries=[UriSpec('user', 'pwd', 'host'),
                                            UriSpec('user', 'pwd', 'host')])
        builder.login_private_registries()
        assert login_mock.call_count == 2

    @mock.patch('docker.APIClient.build')
    def test_build(self, build_mock):
        builder = DockerBuilder(build_context='.',
                                image_name='image',
                                image_tag='tag')
        builder.build()
        assert build_mock.call_count == 1

    @mock.patch('docker.APIClient.push')
    def test_push(self, push_mock):
        builder = DockerBuilder(build_context='.',
                                image_name='image',
                                image_tag='tag')
        builder.push()
        assert push_mock.call_count == 1


class TestBuilder(TestCase):

    @mock.patch('docker.APIClient.build')
    @mock.patch('docker.APIClient.login')
    def test_build_no_login(self, login_mock, build_mock):
        build(build_context='.',
              image_tag='image_tag',
              image_name='image_name',
              nocache=True,
              registries=None)
        assert login_mock.call_count == 0
        assert build_mock.call_count == 1

    @mock.patch('docker.APIClient.build')
    @mock.patch('docker.APIClient.login')
    def test_build_login(self, login_mock, build_mock):
        build(build_context='.',
              image_tag='image_tag',
              image_name='image_name',
              nocache=True,
              registries=[UriSpec('user', 'pwd', 'host'), UriSpec('user', 'pwd', 'host')])
        assert login_mock.call_count == 2
        assert build_mock.call_count == 1

    @mock.patch('docker.APIClient.push')
    @mock.patch('docker.APIClient.build')
    @mock.patch('docker.APIClient.login')
    def test_build_and_push(self, login_mock, build_mock, push_mock):
        build_and_push(build_context='.',
                       image_tag='image_tag',
                       image_name='image_name',
                       nocache=True,
                       registries=[UriSpec('user', 'pwd', 'host'), UriSpec('user', 'pwd', 'host')])
        assert login_mock.call_count == 2
        assert build_mock.call_count == 1
        assert push_mock.call_count == 1

    @mock.patch('docker.APIClient.build')
    def test_build_raise_timeout(self, build_mock):
        build_mock.side_effect = ReadTimeoutError(None, 'foo', 'error')
        with self.assertRaises(BuildException):
            build(build_context='.',
                  image_tag='image_tag',
                  image_name='image_name',
                  nocache=True,
                  max_retries=1,
                  sleep_interval=0)

    @mock.patch('docker.APIClient.push')
    @mock.patch('docker.APIClient.build')
    def test_push_raise_timeout(self, build_mock, push_mock):
        push_mock.side_effect = ReadTimeoutError(None, 'foo', 'error')
        with self.assertRaises(BuildException):
            build_and_push(build_context='.',
                           image_tag='image_tag',
                           image_name='image_name',
                           nocache=True,
                           max_retries=1,
                           sleep_interval=0)
        assert build_mock.call_count == 1
