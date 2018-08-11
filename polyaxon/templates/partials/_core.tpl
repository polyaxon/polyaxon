{{/*
Core config
*/}}
{{- define "config.core" }}
- name: POLYAXON_SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: polyaxon-secret
- name: POLYAXON_INTERNAL_SECRET_TOKEN
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: polyaxon-internal-secret-token
- name: POLYAXON_PASSWORD_LENGTH
  value: {{ default "6" .Values.passwordLength | quote }}
- name: POLYAXON_ENVIRONMENT
{{- if .Values.environment }}
  value:  {{ .Values.environment | quote }}
{{- else }}
  value: "production"
{{- end }}
- name: POLYAXON_TRACKER_BACKEND
  value: "publisher"
- name: POLYAXON_K8S_NODE_NAME
  valueFrom:
    fieldRef:
     fieldPath: spec.nodeName
- name: POLYAXON_K8S_NAMESPACE
  value: {{ .Values.namespace | quote }}
- name: POLYAXON_K8S_GPU_RESOURCE_KEY
{{- if ge (int (include "k8s.minor" .)) 8 }}
  value: "nvidia.com/gpu"
{{- else }}
  value: "alpha.kubernetes.io/nvidia-gpu"
{{- end }}
{{- end -}}
