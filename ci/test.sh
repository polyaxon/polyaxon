#!/bin/sh

set -eux

IP=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')
TEST_NAMESPACE=polyaxon
TEST_URL=http://$IP:31811

kubectl create namespace $TEST_NAMESPACE

helm install --name polyaxon-test --namespace $TEST_NAMESPACE ./polyaxon/ -f ./ci/test-config.yml

echo "waiting for servers to become responsive"
until curl --fail -s $TEST_URL/api/v1/versions/cli/; do
    kubectl --namespace=$TEST_NAMESPACE describe pod
    sleep 10
done

echo "getting polyaxon version"
curl -s $TEST_URL/api/v1/versions/cli/ | grep version
