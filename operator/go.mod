module github.com/polyaxon/polyaxon/operator

go 1.13.12

require (
	github.com/go-logr/logr v0.1.0
	github.com/go-openapi/runtime v0.19.4
	github.com/go-openapi/spec v0.19.3
	github.com/go-openapi/strfmt v0.19.3
	github.com/onsi/ginkgo v1.11.0
	github.com/onsi/gomega v1.8.1
	github.com/polyaxon/polyaxon/sdks v0.0.0-20200620153153-43022ea8589e
	github.com/prometheus/client_golang v0.9.3
	golang.org/x/net v0.0.0-20191004110552-13f9640d40b9
	golang.org/x/sys v0.0.0-20191010194322-b09406accb47 // indirect
	golang.org/x/time v0.0.0-20190308202827-9d24e82272b4 // indirect
	google.golang.org/appengine v1.6.2 // indirect
	k8s.io/api v0.0.0-20191114100352-16d7abae0d2a
	k8s.io/apimachinery v0.0.0-20191028221656-72ed19daf4bb
	k8s.io/client-go v0.0.0-20191114101535-6c5935290e33
	k8s.io/kube-openapi v0.0.0-20190816220812-743ec37842bf
	sigs.k8s.io/controller-runtime v0.4.0
)

// replace github.com/polyaxon/polyaxon/sdks => ../sdks
