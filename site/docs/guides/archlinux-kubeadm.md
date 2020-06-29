---
title: "Install Polyaxon using kubeadm on Kubernetes"
title_link: "Install Polyaxon using kubeadm on Kubernetes"
sub_link: "kubernetes"
date: "2018-10-01"
meta_title: "How to install Polyaxon using kubeadm on Kubernetes"
meta_description: "This is a guide to assist you through the process of setting up a Polyaxon deployment using kubeadm and Kubernetes."
custom_excerpt: "This is a guide to assist you through the process of setting up a Polyaxon deployment using kubeadm and Kubernetes."
featured: false
visibility: public
status: published
tags:
    - guides
    - kubernetes
author:
  name: "jorgemf"
  slug: "jorgemf"
  website: "https://github.com/jorgemf"
  twitter: "jorgemf"
  github: "jorgemf"
---

This file explains how to install polyaxon in kubernetes over archlinux

## Requirements

In `/etc/sysctl.d/99-sysctl.conf` set:
```
net.ipv4.conf.default.rp_filter=1
net.ipv4.conf.all.rp_filter=1
```
If you don't want to reboot do:

```bash
echo 1 > /proc/sys/net/ipv4/conf/default/rp_filter
echo 1 > /proc/sys/net/ipv4/conf/all/rp_filter
```

Install an [aur helper](https://wiki.archlinux.org/index.php/AUR_helpers). We will use `aurman` from now as aur helper. For example:
```bash
git clone https://aur.archlinux.org/aurman.git
cd aurman
makepkg
sudo pacman -U aurman*
```

Install the following packages (some of them are from aur):
* kubelet-bin (1.14.1-0)
* kubeadm-bin (1.14.1-0)
* kubectl-bin (1.14.1-1)
* kubernetes-helm-bin (2.13.1-1)
* docker (1:18.09.6-1)
* nvidia-docker (2.0.3-4)
* etcd-bin
* ethtool

`aurman -S docker etcd-bin kubernetes-helm-bin ethtool nvidia-docker kubelet-bin kubeadm-bin kubectl-bin`

### Add support for nvidia framework to docker

```bash
cat << EOF /tmp/daemon.json
{
    "default-runtime": "nvidia",
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
EOF
sudo cp /tmp/daemon.json /etc/docker/daemon.json
```

Reload, kubeadm drops drop-ins for kubelet, plus the kubernetes-bin package may have had its own
```bash
sudo systemctl daemon-reload
```

## Start kubelet and docker

```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl start kubelet
sudo systemctl enable kubelet
```

## Configure some variables to save typing

This variables depends on the machine you are using. We suppose you have a domain configured that points to your machine IP. We also need to know the local IP of the machine.

```
export POLYAXON_PASSWORD=my_password
export POLYAXON_SERVER=my_server_name
export DOMAIN=my.domain.com
export LOCAL_IP=192.168.0.2
```

## Configure kubernetes

Reset kubernetes for a fresh start

```bash
sudo kubeadm reset
```
### Basic configuration

Init kubernetes. We are using canal so we set the `pod-network-cidr` to the value expecified in the documentation. You might have problems if you are using the same network.

```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```
Move the kubernetes `admin.conf` file to the local user in the machine to use `kubelet`.
```bash
mkdir $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/
sudo chown $(id -u):$(id -g) $HOME/.kube/admin.conf
export KUBECONFIG=$HOME/.kube/admin.conf
```
You might want to add `KUBECONFIG` to your `rc` file.

Wait for few seconds until some containers have been started. You can check them with `kubectl get pods --all-namespaces`

#### Network configuration

Now we configure `canal` for the network in kubernetes.

```bash
kubectl apply -f https://docs.projectcalico.org/v3.5/getting-started/kubernetes/installation/hosted/canal/canal.yaml
```
Wait until `coredns` pods are up and running. Check it with `kubectl get pods --all-namespaces | grep coredns`.

### Untaint master

We can untaint the master node so it can deploy jobs. You must do this if you are only planning to use one node.
```bash
kubectl taint nodes --all node-role.kubernetes.io/master-
```

## Install helm

We need helm in order to install packages

```bash
kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller
```

You should wait until tiller is ready: `kubectl get pods --all-namespaces | grep tiller-deploy`.

### Configure helm repos

we need some repos in helm for the rest of the process. One for polyaxon and another one for `cert-manager`
```bash
helm repo add polyaxon https://charts.polyaxon.com
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

## Add nvidia capabilities

If you use nvidia cards you need to add support for them in kubernetes:

```bash
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/1.0.0-beta/nvidia-device-plugin.yml
```

And wait until the nvidia plugin is ready: `kubectl get pods --all-namespaces | grep nvidia-device`

## Install nginx-stable

Nginx is going to be our ingress controller and we need it to request the certificates for our server and to expose the polyaxon web and api. Review `externalIPs` is you are planning to use more than one machine.

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
cat << EOF > /tmp/service-nodeport.yaml
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
spec:
  externalTrafficPolicy: Local
  type: NodePort
  externalIPs:
    - LOCAL_IP
  ports:
    - name: http
      port: 80
      targetPort: 80
      protocol: TCP
    - name: https
      port: 443
      targetPort: 443
      protocol: TCP
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
---
EOF
kubectl apply -f /tmp/service-nodeport.yaml
```

We can checkk `nginx` is working and it has an IP:
```bash
kubectl get svc
```

## Install cert-manager

We will use `cert-manager` for our machine to requests signed certificates. That will add support for ssl. For more information see https://docs.cert-manager.io/en/latest/tutorials/acme/quick-start/index.html

```bash
kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.7/deploy/manifests/00-crds.yaml
kubectl create namespace cert-manager
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true

helm install --name cert-manager --namespace cert-manager --version v0.7.2 jetstack/cert-manager
```

Wait until cert-manager is ready: `kubectl get pods --namespace cert-manager | grep webhook`

### Configure the Issuer for polyaxon

Check the `contact email`. You will receive emails related with your certificates there. You should also test with the staging acme server first. We only set here the production acme server.

```bash
cat <<EOF > /tmp/cert-pod.yaml
apiVersion: certmanager.k8s.io/v1alpha1
kind: Issuer
metadata:
  name: letsencrypt-prod
  namespace: polyaxon
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: contact@$DOMAIN
    privateKeySecretRef:
      name: letsencrypt-prod
    http01: {}
---
EOF
kubectl apply -f /tmp/cert-pod.yaml
```

Wait until the issuer is ready: `kubectl describe issuer letsencrypt-prod --namespace polyaxon`

## Using local directories for all nodes of polyaxon

### Configure the nfs directory:

We can add nfs directories to our configuration in case we want to share those directories with all the cluster.

https://wiki.archlinux.org/index.php/NFS#Server

Our nfs directories are `/srv/nfs/data/` and `/srv/nfs/outputs`.

In `/etc/exports`:
```
/srv/nfs/data       127.0.0.0/16(rw,sync) 
/srv/nfs/outputs    127.0.0.0/16(rw,sync)
```

Update it with `sudo exportsfs -a`

Start and enable the service:

```bash
sudo systemctl enable nfs-server.service
sudo systemctl start nfs-server.service
```
### Create persistence volumes for our nfs directories

Adjuts the `storage` values as needed

```bash
cat <<EOF > /tmp/pvcdata.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: polyaxon-pv-data
spec:
  capacity:
    storage: 3Ti
  accessModes:
    - ReadWriteMany
  nfs:
    path: /srv/nfs/data
    server: $POLYAXON_SERVER
    readOnly: false
  claimRef:
    namespace: polyaxon
    name: polyaxon-pvc-data
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name:  polyaxon-pvc-data
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 3Ti
EOF
kubectl create --namespace=polyaxon -f /tmp/pvcdata.yaml

cat <<EOF > /tmp/pvcoutputs.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: polyaxon-pv-outputs
spec:
  capacity:
    storage: 256Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /srv/nfs/outputs
    server: $POLYAXON_SERVER
    readOnly: false
  claimRef:
    namespace: polyaxon
    name: polyaxon-pvc-outputs
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name:  polyaxon-pvc-outputs
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 256Gi
EOF
kubectl create --namespace=polyaxon -f /tmp/pvcoutputs.yaml
```
Wait until the volumes are ready: `kubectl get pv polyaxon-pvc-data` and `kubectl get pv polyaxon-pvc-outputs`

## Install polyaxon

More info in: https://install.polyaxon.com/deploy

```bash
cat <<EOF > /tmp/polyaxon.conf
user:
  username: root
  email: root@polyaxon.local
  password: $POLYAXON_PASSWORD
rbac:
  enabled: true
serviceType: ClusterIP
ingress:
  enabled: true
  hostName: $DOMAIN
  tls:
  - secretName: polyaxon-letsencrypt
    hosts:
    - $DOMAIN
  annotations:
    certmanager.k8s.io/issuer: letsencrypt-prod
api:
  service:
    annotations:
      domainName: $DOMAIN
persistence:
  data:
    data:
      existingClaim: polyaxon-pvc-data
      mountPath: /data
  outputs:
    output:
      existingClaim: polyaxon-pvc-outputs
      mountPath: /outputs
EOF

helm install polyaxon/polyaxon --name=polyaxon --namespace=polyaxon -f /tmp/polyaxon.conf
```

To upgrade polyaxon in the future you can run:
```bash
helm upgrade polyaxon polyaxon/polyaxon --namespace=polyaxon -f /tmp/polyaxon.conf
```

Now wait until polyaxon is ready: `kubectl get pods --namespace=polyaxon | grep polyaxon-api`

## Install and configure client
```bash
pip install polyaxon-cli
polyaxon config set --host=$DOMAIN --verbose=false --port=443 --use_https=true --verify_ssl=true
```

Check everything is working:
```bash
polyaxon login -u root -p $POLYAXON_PASSWORD
polyaxon cluster
```
