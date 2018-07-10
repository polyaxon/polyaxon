#!/bin/bash
while [ "$(python3 ./manage.py showmigrations --plan | grep '\[ \]\|^[a-z]' | grep '[  ]' -B 1)" ]; do echo "Preparing..."; sleep 60; done; echo "Running...";
