[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://travis-ci.org/polyaxon/rhea.svg?branch=master)](https://travis-ci.org/polyaxon/rhea)
[![PyPI version](https://badge.fury.io/py/rhea.svg)](https://badge.fury.io/py/rhea)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e49f4132c90e496e974d3e9883ee4d8c)](https://www.codacy.com/app/polyaxon/rhea?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=polyaxon/rhea&amp;utm_campaign=Badge_Grade)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)

# rhea

Efficient environment variables management and typing for python.

## Installation

```
pip install -U rhea
```

## Features 

 * Typed retrieval of environment variables.
 * Handling of optional, secret, and local variables.
 * Reading from different sources: os, json files, yaml files.
 * Collection of parsed parameters.

## Usage

### Reading typed values from a params


```python
from rhea import Rhea

rhea_config = Rhea(bool_value1='1', 
                   bool_value2='false', 
                   bool_value3=True)
                   
rhea_config.get_boolean('bool_value1')
# True

rhea_config.get_boolean('bool_value2')
# False

rhea_config.get_boolean('bool_value3')
# True
```

### Reading typed values from a env vars


```python
import os

from rhea import Rhea

rhea_config = Rhea.read_configs(os.environ)
```

### Reading typed values from different sources

```python
import os

from rhea import Rhea

rhea_config = Rhea.read_configs([os.environ, 
                                'json_file.json', 
                                'yaml_file.yaml',
                                'another_file_override.json',
                                {'foo': 'bar'}])
```

### Base types

examples:

```
BOOL_ENV_VALUE1: 1
BOOL_ENV_VALUE2: true
BOOL_ENV_VALUE3: f
BOOL_ENV_VALUE4: on

INT_ENV_VALUE1: '1' 
INT_ENV_VALUE2: -100

STRING_ENV_VALUE: 'some string'

FLOAT_ENV_VALUE1: '1.1'
FLOAT_ENV_VALUE2: -1.3
FLOAT_ENV_VALUE3: 1111.1
FLOAT_ENV_VALUE4: -33

DICT_ENV_VALUE: {"foo": "bar", "1": "2"}

LIST_ENV_VALUE: 'foo, bar, boo'

URI_ENV_VALUE1: user:pass@host.com
URI_ENV_VALUE2: user:pass@host:4000

AUTH_ENV_VALUE: user:pass
```

Reading:

```python
from rhea import Rhea

rhea_config = Rhea.read_configs([...])

rhea_config.get_boolean('BOOL_ENV_VALUE1')
# True
rhea_config.get_boolean('BOOL_ENV_VALUE2')
# True
rhea_config.get_boolean('BOOL_ENV_VALUE3')
# False
rhea_config.get_boolean('BOOL_ENV_VALUE4')
# True

rhea_config.get_int('INT_ENV_VALUE1')  
# 1
rhea_config.get_int('INT_ENV_VALUE2')  
# -100

rhea_config.get_string('STRING_ENV_VALUE')  
# some string

rhea_config.get_float('FLOAT_ENV_VALUE1')
# 1.1
rhea_config.get_float('FLOAT_ENV_VALUE1')
# -1.3
rhea_config.get_float('FLOAT_ENV_VALUE1')
# 1111.1
rhea_config.get_float('FLOAT_ENV_VALUE1')
# -33.0

rhea_config.get_dict('DICT_ENV_VALUE')
# {'foo': 'bar', '1': '2'}

rhea_config.get_list('LIST_ENV_VALUE')
# ['foo', 'bar', 'boo']

rhea_config.get_uri('URI_ENV_VALUE1')
# UriSpec('user', 'pass', 'host')

rhea_config.get_uri('URI_ENV_VALUE2')
# UriSpec('user', 'pass', 'host:4000')

rhea_config.get_uri('AUTH_ENV_VALUE')
# AuthSpec('user', 'pass')
```

### List of base types

examples:

```
BOOLS_ENV_VALUE: '[1, 0, "true", "false", "t", "f", "on", "off"]'
INTS_ENV_VALUE: '[1, 0, -100]'
STRINGS_ENV_VALUE: '["some_string", "another_string"]'
FLOATS_ENV_VALUE: '[1.1, -1.3, 0.03, 1111.1, 1.]'
DICTS_ENV_VALUE: '[{"foo": "bar", "1": 2}, {"foo": "bar", "1": 2}]'
DICT_OF_DICTS_ENV_VALUE: '{"key1": {"foo": "bar", "1": 2}, "key2": {"foo": "bar", "1": 2}}'
URIS_ENV_VALUE: '["user:pass@host.com", "user:pass@host:4000"]'
AUTHS_ENV_VALUE: '["user1:pass1", "user2:pass2"]'
```

Reading:

```python
from rhea import Rhea

rhea_config = Rhea.read_configs([...])

rhea_config.get_boolean('BOOLS_ENV_VALUE', is_list=True)
#  [True, False, True, False, True, False, True, False]

rhea_config.get_int('INTS_ENV_VALUE', is_list=True)
# [1, 0, -100]

rhea_config.get_string('STRINGS_ENV_VALUE', is_list=True)
# ['some_string', 'another_string']

rhea_config.get_float('FLOATS_ENV_VALUE', is_list=True)
# [1.1, -1.3, 0.03, 1111.1, 1.0]

rhea_config.get_dict('DICTS_ENV_VALUE', is_list=True)
# [{'foo1': 'bar1', '1': 2}, {'foo2': 'bar2', '3': 4}]

rhea_config.get_dict_of_dicts('DICT_OF_DICTS_ENV_VALUE')
# {'key1': {'foo': 'bar', '1': 2}, 'key2': {'foo': 'bar', '1': 2}}

rhea_config.get_uri('URIS_ENV_VALUE', is_list=True)
# [UriSpec('user', 'pass', 'host'), UriSpec('user', 'pass', 'host:4000')]

rhea_config.get_uri('AUTHS_ENV_VALUE', is_list=True)
# [UriSpec('user1', 'pass1'), UriSpec('user2', 'pass2')]
```

### Optional values and default values


```python
from rhea import Rhea

rhea_config = Rhea.read_configs([...])

rhea_config.get_boolean('BOOL_ENV_VALUE', is_optional=True)
# None
rhea_config.get_boolean('BOOL_ENV_VALUE', is_optional=True, default=True)
# True

rhea_config.get_int('INT_ENV_VALUE', is_optional=True)
# None
rhea_config.get_int('INT_ENV_VALUE', is_optional=True, default=101)
# 101

rhea_config.get_float('FLOAT_ENV_VALUE', is_optional=True)
# None
rhea_config.get_float('FLOAT_ENV_VALUE', is_optional=True, default=-3.3)
# -3.3

rhea_config.get_float('STRING_ENV_VALUE', is_optional=True)
# None
rhea_config.get_float('STRING_ENV_VALUE', is_optional=True, default='default')
# default
```

### Value validation


```python
from rhea import Rhea

rhea_config = Rhea.read_configs([...])


# INT_ENV_VALUE = 11
rhea_config.get_int('INT_ENV_VALUE', options=[1, 2, 3])
# raise RheaError
rhea_config.get_int('INT_ENV_VALUE', options=[1, 2, 3, 11])
# 11
```

### Parsed data


```python
from rhea import Rhea

rhea_config = Rhea.read_configs([...])

rhea_config.get_requested_data(include_locals=False, include_secrets=False)
# {'key1': 'value1', ...}
```

## Example with Django

```python
from rhea import Rhea

rhea_config = Rhea.read_configs([...])

DEBUG = rhea_config.get_boolean('DJANGO_DEBUG_MODE', is_optional=True, default=False)
SECRET_KEY = rhea_config.get_string('POLYAXON_SECRET_KEY', is_secret=True)
```

## Running tests

```
pytest
```

# License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpolyaxon%2Frhea.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fpolyaxon%2Frhea?ref=badge_large)
