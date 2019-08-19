module github.com/polyaxon/polyaxon-operator

go 1.12

require (
	github.com/emicklei/go-restful v2.9.6+incompatible // indirect
	github.com/go-logr/logr v0.1.0
	github.com/go-openapi/runtime v0.19.4
	github.com/go-openapi/strfmt v0.19.2
	github.com/kubeflow/mpi-operator v0.2.1
	github.com/kubeflow/pytorch-operator v0.5.1
	github.com/kubeflow/tf-operator v0.5.3
	github.com/onsi/ginkgo v1.8.0
	github.com/onsi/gomega v1.5.0
	github.com/polyaxon/polyaxon-sdks v0.0.0-20190819113418-6ab4b411ef48
	github.com/sirupsen/logrus v1.4.2 // indirect; indirect (kf stuff)
	k8s.io/api v0.0.0-20190409021203-6e4e0e4f393b
	k8s.io/apimachinery v0.0.0-20190404173353-6a84e37a896d
	k8s.io/client-go v11.0.1-0.20190409021438-1a26190bd76a+incompatible
	sigs.k8s.io/controller-runtime v0.2.0-beta.4
	sigs.k8s.io/controller-tools v0.2.0-beta.5 // indirect
)
