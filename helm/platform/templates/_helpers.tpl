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
