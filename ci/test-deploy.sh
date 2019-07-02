#!/bin/sh

set -eux

#!/bin/sh

set -eux

# Is there a standard interface name?
for iface in eth0 ens4 enp0s3; do
    IP=$(ifconfig $iface | grep 'inet addr' | cut -d: -f2 | awk '{print $1}');
    if [ -n "$IP" ]; then
        echo "IP: $IP"
        break
    fi
done
if [ -z "$IP" ]; then
    echo "Failed to get IP, current interfaces:"
    ifconfig -a
    exit 2
fi

TEST_NAMESPACE=polyaxon
TEST_URL=http://$IP:31811

echo "create namespace"
kubectl create namespace $TEST_NAMESPACE

echo "deploy polyaxon"
helm install --name polyaxon-test --namespace $TEST_NAMESPACE ./polyaxon/ -f ./ci/test-config.yml

echo "waiting for servers to become responsive"
until curl --fail -s $TEST_URL/api/v1/versions/cli/; do
    kubectl --namespace=$TEST_NAMESPACE get pod
    sleep 10
done

echo "getting polyaxon version"
curl -s $TEST_URL/api/v1/versions/cli/ | grep version


echo "running tests"

display_logs() {
  echo "***** minikube *****"
  minikube logs
  echo "***** node *****"
  kubectl describe node
  echo "***** pods *****"
  kubectl --namespace $TEST_NAMESPACE get pods
  echo "***** events *****"
  kubectl --namespace $TEST_NAMESPACE get events
  echo "***** hub *****"
  kubectl --namespace $TEST_NAMESPACE logs deploy/hub
  echo "***** proxy *****"
  kubectl --namespace $TEST_NAMESPACE logs deploy/proxy
}

echo "configure cli"
polyaxon config set --host=$IP --port=31811 | grep updated
echo "cli login"
polyaxon login -u travis -p travis | grep success
echo "cli create project"
polyaxon project create --name=travis-test --description='Travis testing' | grep success
echo "cli init project"
polyaxon project -p travis-test git --url=https://github.com/polyaxon/polyaxon-quick-start | grep success
