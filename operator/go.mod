module github.com/polyaxon/polyaxon/operator

go 1.15

require (
	github.com/go-logr/logr v0.3.0
	github.com/go-openapi/runtime v0.19.24
	github.com/go-openapi/spec v0.20.0
	github.com/go-openapi/strfmt v0.19.11
	github.com/onsi/ginkgo v1.14.2
	github.com/onsi/gomega v1.10.4
	github.com/polyaxon/polyaxon/sdks v0.0.0-20201217174509-04eb3e26fa17
	github.com/prometheus/client_golang v1.7.1
	golang.org/x/net v0.0.0-20201202161906-c7110b5ffcbb
	k8s.io/api v0.19.2
	k8s.io/apimachinery v0.19.2
	k8s.io/client-go v0.19.2
	k8s.io/kube-openapi v0.0.0-20200805222855-6aeccd4b50c6
	sigs.k8s.io/controller-runtime v0.7.0
)

// replace github.com/polyaxon/polyaxon/sdks => ../sdks
