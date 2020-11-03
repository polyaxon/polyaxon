module github.com/polyaxon/polyaxon/operator

go 1.13.12

require (
	github.com/go-logr/logr v0.1.0
	github.com/go-openapi/runtime v0.19.23
	github.com/go-openapi/spec v0.19.8
	github.com/go-openapi/strfmt v0.19.8
	github.com/onsi/ginkgo v1.11.0
	github.com/onsi/gomega v1.8.1
	github.com/polyaxon/polyaxon/sdks v0.0.0-20201101150555-f6afa18976f4
	github.com/prometheus/client_golang v0.9.3
	golang.org/x/net v0.0.0-20200602114024-627f9648deb9
	k8s.io/api v0.0.0-20191114100352-16d7abae0d2a
	k8s.io/apimachinery v0.0.0-20191028221656-72ed19daf4bb
	k8s.io/client-go v0.0.0-20191114101535-6c5935290e33
	k8s.io/kube-openapi v0.0.0-20190816220812-743ec37842bf
	sigs.k8s.io/controller-runtime v0.4.0
)

// replace github.com/polyaxon/polyaxon/sdks => ../sdks
