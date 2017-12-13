# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import click
import six
from tabulate import tabulate


def get_meta_response(response):
    results = {}
    if response.get('next'):
        results['next'] = '--page={}'.format(response['next'])
    if response.get('previous'):
        results['previous'] = '--page={}'.format(response['previous'])
    if response.get('count'):
        results['count'] = response['count']
    return results


def list_dicts_to_tabulate(list_dicts):
    results = OrderedDict()
    for d_value in list_dicts:
        for k, v in six.iteritems(d_value):
            if k in results:
                results[k].append(v)
            else:
                results[k] = [v]

    return results


def dict_tabulate(dict_value, is_list_dict=False):
    if is_list_dict:
        headers = six.iterkeys(dict_value)
        click.echo(tabulate(dict_value, headers=headers))
    else:
        click.echo(tabulate(six.iteritems(dict_value)))


class Printer(object):
    @staticmethod
    def print_header(text):
        click.secho('\n{}\n'.format(text), fg='yellow')

    @staticmethod
    def print_warning(text):
        click.secho('\n{}\n'.format(text), fg='magenta')

    @staticmethod
    def print_success(text):
        click.secho('\n{}\n'.format(text), fg='green')

    @staticmethod
    def print_error(text):
        click.secho('\n{}\n'.format(text), fg='red')
