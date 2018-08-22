#!/bin/sh

set -eux

IP=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}')
TEST_NAMESPACE=polyaxon-test
TEST_URL=http://$IP:31811

helm install --name polyaxon-test --namespace $TEST_NAMESPACE ./polyaxon/ -f ./ci/test-config.yaml

echo "waiting for servers to become responsive"
until curl --fail -s $TEST_URL/api/v1/versions/cli/; do
    kubectl --namespace=$TEST_NAMESPACE describe pod
    sleep 10
done

echo "getting polyaxon version"
curl -s $TEST_URL/api/v1/versions/cli/ | grep version
