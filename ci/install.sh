#!/bin/bash
set -ex

mkdir -p bin

# install nsenter if missing (needed by kube on trusty)
if ! which nsenter; then
  curl -L https://github.com/minrk/git-crypt-bin/releases/download/trusty/nsenter > nsenter
  echo "5652bda3fbea6078896705130286b491b6b1885d7b13bda1dfc9bdfb08b49a2e  nsenter" | shasum -a 256 -c -
  chmod +x nsenter
  sudo mv nsenter /usr/local/bin/
fi

echo "installing kubectl"
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v${KUBE_VERSION}/bin/linux/amd64/kubectl
chmod +x kubectl
sudo cp kubectl /usr/local/bin/
mv kubectl bin/

echo "installing minikube"
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v${MINIKUBE_VERSION}/minikube-linux-amd64
chmod +x minikube
sudo cp minikube /usr/local/bin/
mv minikube bin/


echo "starting minikube with RBAC"
sudo CHANGE_MINIKUBE_NONE_USER=true $PWD/bin/minikube start --vm-driver=none --kubernetes-version=v${KUBE_VERSION} --extra-config=apiserver.Authorization.Mode=RBAC --bootstrapper=localkube
minikube update-context

echo "waiting for kubernetes"
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'
until kubectl get nodes -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"; do
  sleep 1
done
kubectl get nodes

minikube addons list
sudo CHANGE_MINIKUBE_NONE_USER=true $PWD/bin/minikube addons enable coredns

echo "installing helm"
curl -ssL https://storage.googleapis.com/kubernetes-helm/helm-v${HELM_VERSION}-linux-amd64.tar.gz \
  | tar -xz -C bin --strip-components 1 linux-amd64/helm
chmod +x bin/helm

kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller


echo "waiting for tiller"
kubectl --namespace=kube-system rollout status --watch deployment/tiller-deploy

echo "Install dep"
helm repo add polyaxon https://charts.polyaxon.com
helm repo update

echo "Install CLI"
pip3 install -r ./ci/requirements.txt
