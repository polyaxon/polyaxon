{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "polyaxon.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "polyaxon.fullname" -}}
{{- printf "%s-%s" .Release.Name "polyaxon" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "k8s.minor" -}}
{{ .Capabilities.KubeVersion.Minor |  trimSuffix "+" }}
{{- end -}}


{{/*
Return the appropriate apiVersion for networkpolicy.
*/}}
{{- define "networkPolicy.apiVersion" -}}
{{- if and (ge (int (include "k8s.minor" .)) 4) (le (int (include "k8s.minor" .)) 6) -}}
"extensions/v1beta1"
{{- else if ge (int (.Capabilities.KubeVersion.Minor)) 7 -}}
"networking.k8s.io/v1"
{{- end -}}
{{- end -}}
