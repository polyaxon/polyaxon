[![Build Status](https://travis-ci.org/polyaxon/polyaxon.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon-api)
[![PyPI version](https://badge.fury.io/py/polyaxon.svg)](https://badge.fury.io/py/polyaxon)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/polyaxon/polyaxon)

# Polyaxon-api

Polyaxon-api aims to provide a web-api to create, store, run, and compare polyaxon experiments. 

The project depends on [polyaxon](https://github.com/polyaxon/polyaxon) the library. 

# Installation

Clone the repo `git clone https://github.com/polyaxon/polyaxon-api.git`, and use the commands to do everything in docker:
 
 * `cmd/rebuild` to build the docker containers.
 * `cmd/setup` to setup the depenedencis, initialize the databas and run migrations.
 * `cmd/runserver` to run the web server.
 * `cmd/manage` to access to the django manage. For example you can run `cmd/manage makemigrations core` to create the necessary migrations after changing the code.
 * `cmd/jupyter` to start a jupyter notebook server.
 * `cmd/tensorboard` to start a tensorboard server.
 * `cmd/test` to run the tests.   

# Project status

Polyaxon-api is in a pre-release "alpha" state. All interfaces, programming interfaces, and data structures may be changed without prior notice.
We'll do our best to communicate potentially disruptive changes.

# Contributions

Please follow the contribution guide line: *[Contribute to Polyaxon](CONTRIBUTING.md)*.

# License

MIT License
