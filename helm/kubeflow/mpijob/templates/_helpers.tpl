{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "mpijob.fullname" -}}
{{- printf "%s-%s" .Release.Name "tf-job" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "type" -}}
{{- "polyaxon-integration" -}}
{{- end -}}

{{- define "roles.config" -}}
{{- "polyaxon-config" -}}
{{- end -}}

{{- define "roles.worker" -}}
{{- "polyaxon-workers" -}}
{{- end -}}
