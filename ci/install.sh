#!/bin/bash
set -ex

mkdir -p bin

# nsenter is included on xenial

# install socat (required by helm)
sudo apt-get update && sudo apt-get install -y socat

# install kubectl, minikube
# based on https://blog.travis-ci.com/2017-10-26-running-kubernetes-on-travis-ci-with-minikube
echo "installing kubectl"
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v${KUBE_VERSION}/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl bin/

echo "installing minikube"
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v${MINIKUBE_VERSION}/minikube-linux-amd64
chmod +x minikube
mv minikube bin/
# Reduce CI logs clutter
bin/minikube config set WantKubectlDownloadMsg false
bin/minikube config set WantReportErrorPrompt false

# FIXME: Workaround missing crictl on K8s 1.11 only
if [ ! -z "${CRICTL_VERSION}" ]; then
  echo "installing crictl"
  if ! [ -f bin/crictl-${CRICTL_VERSION} ]; then
    curl -sSLo bin/crictl-${CRICTL_VERSION}.tar.gz https://github.com/kubernetes-sigs/cri-tools/releases/download/v${CRICTL_VERSION}/crictl-v${CRICTL_VERSION}-linux-amd64.tar.gz
    tar --extract --file bin/crictl-${CRICTL_VERSION}.tar.gz --directory bin
    rm bin/crictl-${CRICTL_VERSION}.tar.gz
    mv bin/crictl bin/crictl-${CRICTL_VERSION}
  fi
  cp bin/crictl-${CRICTL_VERSION} bin/crictl
  # minikube is run with sudo so the modified PATH is lost
  sudo ln -s "${PWD}/bin/crictl-${CRICTL_VERSION}" /usr/bin/crictl
fi


echo "installing kubeval"
if ! [ -f bin/kubeval-${KUBEVAL_VERSION} ]; then
  curl -sSLo bin/kubeval-${KUBEVAL_VERSION}.tar.gz https://github.com/garethr/kubeval/releases/download/${KUBEVAL_VERSION}/kubeval-linux-amd64.tar.gz
  tar --extract --file bin/kubeval-${KUBEVAL_VERSION}.tar.gz --directory bin
  rm bin/kubeval-${KUBEVAL_VERSION}.tar.gz
  mv bin/kubeval bin/kubeval-${KUBEVAL_VERSION}
fi
cp bin/kubeval-${KUBEVAL_VERSION} bin/kubeval

echo "starting minikube with RBAC"
sudo CHANGE_MINIKUBE_NONE_USER=true $PWD/bin/minikube start $MINIKUBE_ARGS
minikube update-context

# If using CNI the node will not be NotReady until a CNI config exists
if [ "$INSTALL_CALICO" = "1" ]; then
  echo "installing calico"
  # https://github.com/projectcalico/calico/issues/1456#issuecomment-422957446
  kubectl apply -f https://docs.projectcalico.org/v3.3/getting-started/kubernetes/installation/hosted/etcd.yaml
  kubectl apply -f https://docs.projectcalico.org/v3.3/getting-started/kubernetes/installation/rbac.yaml
  curl -sf https://docs.projectcalico.org/v3.3/getting-started/kubernetes/installation/hosted/calico.yaml -O
  CALICO_ETCD_IP=$(kubectl get service --namespace=kube-system calico-etcd -o jsonpath='{.spec.clusterIP}')
  sed -i -e "s/10\.96\.232\.136/$CALICO_ETCD_IP/" calico.yaml
  kubectl apply -f calico.yaml

  echo "waiting for calico"
  JSONPATH='{.status.numberReady}'
  until [ "$(kubectl get daemonsets calico-node -n kube-system -o jsonpath="$JSONPATH")" = "1" ]; do
    sleep 1
  done
fi

echo "waiting for kubernetes"
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'
until kubectl get nodes -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"; do
  sleep 1
done
kubectl get nodes

echo "installing helm"
curl -ssL https://storage.googleapis.com/kubernetes-helm/helm-v${HELM_VERSION}-linux-amd64.tar.gz \
  | tar -xz -C bin --strip-components 1 linux-amd64/helm
chmod +x bin/helm

kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller


echo "waiting for tiller"
kubectl --namespace=kube-system rollout status --watch deployment/tiller-deploy

echo "installing git-crypt"
curl -L https://github.com/minrk/git-crypt-bin/releases/download/0.5.0/git-crypt > bin/git-crypt
echo "46c288cc849c23a28239de3386c6050e5c7d7acd50b1d0248d86e6efff09c61b  bin/git-crypt" | shasum -a 256 -c -
chmod +x bin/git-crypt

echo "Install dep"
helm repo add polyaxon https://charts.polyaxon.com
helm repo update

echo "Install CLI"
pip3 install -r ./ci/requirements.txt
