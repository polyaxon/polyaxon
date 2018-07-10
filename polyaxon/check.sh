#!/bin/bash
while [ ! "$(ptyhon3 ./manage.py showmigrations --plan | grep '\[ \]\|^[a-z]' | grep '[  ]' -B 1)" ]; do echo "Waiting for migrations..."; sleep 60; done;
