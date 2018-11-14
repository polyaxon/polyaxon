#!/bin/bash
while [ "$(python3.7 /polyaxon/polyaxon/manage.py showmigrations --plan | grep '\[ \]\|^[a-z]' | grep '[  ]' -B 1)" ]; do echo "Preparing..."; sleep 60; done; echo "Running...";
