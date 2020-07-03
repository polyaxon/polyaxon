{{- /*
Config labels common
*/}}
{{- define "config.labels.common" -}}
release: "{{ .Release.Name }}"
heritage: "{{ .Release.Service }}"
app.kubernetes.io/instance: "{{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}"
app.kubernetes.io/version: "{{ .Chart.Version }}"
app.kubernetes.io/managed-by: "helm"
{{- end -}}

{{- /*
Config labels roles core api
*/}}
{{- define "config.labels.roles.coreApi" -}}
app.kubernetes.io/part-of: "polyaxon-core"
app.kubernetes.io/component: "polyaxon-api"
{{- end -}}

{{- /*
Config labels roles core worker
*/}}
{{- define "config.labels.roles.coreWorker" -}}
app.kubernetes.io/part-of: "polyaxon-core"
app.kubernetes.io/component: "polyaxon-workers"
{{- end -}}

{{- /*
Config labels roles core helpers
*/}}
{{- define "config.labels.roles.coreHelpers" -}}
app.kubernetes.io/part-of: "polyaxon-core"
app.kubernetes.io/component: "polyaxon-helpers"
{{- end -}}

{{- /*
Config labels roles core agent
*/}}
{{- define "config.labels.roles.coreAgent" -}}
app.kubernetes.io/part-of: "polyaxon-core"
app.kubernetes.io/component: "polyaxon-agent"
{{- end -}}

{{- /*
Config labels role core config
*/}}
{{- define "config.labels.roles.coreConfig" -}}
app.kubernetes.io/part-of: "polyaxon-core"
app.kubernetes.io/component: "polyaxon-config"
{{- end -}}

{{- /*
Config labels role core hooks
*/}}
{{- define "config.labels.roles.coreHooks" -}}
app.kubernetes.io/part-of: "polyaxon-core"
app.kubernetes.io/component: "polyaxon-hooks"
{{- end -}}

{{- /*
Config labels apps gateway
*/}}
{{- define "config.labels.apps.gateway" -}}
app.kubernetes.io/name: {{ template "polyaxon.fullname" . }}-gateway
{{- end -}}

{{- /*
Config labels apps streams
*/}}
{{- define "config.labels.apps.streams" -}}
app.kubernetes.io/name: {{ template "polyaxon.fullname" . }}-streams
{{- end -}}
