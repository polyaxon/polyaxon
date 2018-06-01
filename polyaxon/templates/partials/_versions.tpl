{{/*
versions config
*/}}
{{- define "config.versions" }}
- name: POLYAXON_CLI_MIN_VERSION
  value: "0.0.8"
- name: POLYAXON_CLI_LATEST_VERSION
  value: "0.1.0"
- name: POLYAXON_PLATFORM_MIN_VERSION
  value: "0.0.9"
- name: POLYAXON_PLATFORM_LATEST_VERSION
  value: "0.1.0"
- name: POLYAXON_LIB_MIN_VERSION
  value: "0.0.2"
- name: POLYAXON_LIB_LATEST_VERSION
  value: "0.0.5"
- name: POLYAXON_CHART_VERSION
  value: {{ .Chart.Version | quote }}
- name: POLYAXON_CHART_IS_UPGRADE
  value: {{ .Release.IsUpgrade | quote }}
- name: POLYAXON_CHART_REVISION
  value: {{ .Release.Revision | quote }}
{{- end -}}
