module github.com/polyaxon/polyaxon/operator

go 1.13

require (
	github.com/go-logr/logr v0.1.0
	github.com/go-openapi/runtime v0.19.4
	github.com/go-openapi/spec v0.19.3
	github.com/go-openapi/strfmt v0.19.2
	github.com/golang/groupcache v0.0.0-20190702054246-869f871628b6 // indirect
	github.com/google/go-cmp v0.3.1 // indirect
	github.com/konsorten/go-windows-terminal-sequences v1.0.2 // indirect
	github.com/kubeflow/common v0.0.0-20200116014622-88a0cd071cf1 // indirect
	github.com/kubeflow/mpi-operator v0.2.2 // indirect
	github.com/kubeflow/pytorch-operator v0.6.0 // indirect
	github.com/kubeflow/tf-operator v0.5.3 // indirect
	github.com/onsi/ginkgo v1.10.2
	github.com/onsi/gomega v1.7.0
	github.com/polyaxon/polyaxon/sdks v0.0.0-20191228091608-ea5d46937880
	github.com/prometheus/client_golang v0.9.3
	golang.org/x/net v0.0.0-20191004110552-13f9640d40b9
	golang.org/x/sys v0.0.0-20191010194322-b09406accb47 // indirect
	google.golang.org/appengine v1.6.2 // indirect
	k8s.io/api v0.0.0-20191114100352-16d7abae0d2a
	k8s.io/apimachinery v0.0.0-20191028221656-72ed19daf4bb
	k8s.io/client-go v0.0.0-20191114101535-6c5935290e33
	k8s.io/kube-openapi v0.0.0-20190816220812-743ec37842bf
	sigs.k8s.io/controller-runtime v0.4.0
)

replace github.com/polyaxon/polyaxon/sdks => ../sdks
