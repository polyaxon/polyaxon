#!/usr/bin/env bash
if [ $# -lt 1 ]
  then
    echo "You should provide at least 1 args: branch"
     exit 1
fi

if [ "$1" == "master" ]
    then
        body='{
        "request": {
        "branch":master
        }}'

        curl -s -X POST \
           -H "Content-Type: application/json" \
           -H "Accept: application/json" \
           -H "Travis-API-Version: 3" \
           -H "Authorization: token 6SE268-eR1WMZUTvmYjUrg" \
           -d "$body" \
           https://api.travis-ci.org/repo/polyaxon%2Fpolyaxon-docker/requests
fi
