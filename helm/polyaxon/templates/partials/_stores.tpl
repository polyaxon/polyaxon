{{- /*
Config artifacts store secrets/configmap
*/}}
{{- define "config.artifactsStore.envFrom" -}}
{{- if and .Values.artifactsStore }}
{{- if .Values.artifactsStore.secret }}
{{- if (empty .Values.artifactsStore.secret.mountPath) }}
- secretRef:
    name: {{ .Values.artifactsStore.secret.name | quote }}
{{- end }} {{- /* endif */ -}}
{{- end }} {{- /* endif */ -}}
{{- if .Values.artifactsStore.configMap }}
{{- if (empty .Values.artifactsStore.configMap.mountPath) }}
- configMapRef:
    name: {{ .Values.artifactsStore.configMap.name | quote }}
{{- end }} {{- /* endif */ -}}
{{- end }} {{- /* endif */ -}}
{{- end }} {{- /* endif artifactsStore */ -}}
{{- end -}} {{- /* end def artifactsStore envFrom */ -}}

{{- define "config.artifactsStore.mount" -}}
{{- if and .Values.artifactsStore }}
{{- if or (eq .Values.artifactsStore.kind "host_path") (eq .Values.artifactsStore.kind "volume_claim") }}
- mountPath: {{ .Values.artifactsStore.schema.mountPath | quote }}
  name: {{ .Values.artifactsStore.name }}
  {{ if .Values.artifactsStore.schema.subPath -}}
  subPath: {{ .Values.artifactsStore.schema.subPath | quote }}
  {{- end }}
{{- end }}
{{- if .Values.artifactsStore.secret }}
{{- if .Values.artifactsStore.secret.mountPath }}
- mountPath: {{ .Values.artifactsStore.secret.mountPath | quote }}
  name: {{ .Values.artifactsStore.secret.name | quote }}
  readOnly: true
{{- end }}
{{- end }}
{{- if .Values.artifactsStore.configMap }}
{{- if .Values.artifactsStore.configMap.mountPath }}
- mountPath: {{ .Values.artifactsStore.configMap.mountPath | quote }}
  name: {{ .Values.artifactsStore.configMap.name | quote }}
  readOnly: true
{{- end }}
{{- end }}
{{- end }} {{- /* endif artifactsStore */ -}}
{{- end -}} {{- /* end def artifactsStore volume mounts */ -}}

{{- define "config.artifactsStore.volume" -}}
{{- if and .Values.artifactsStore }}
{{- if or (eq .Values.artifactsStore.kind "host_path") (eq .Values.artifactsStore.kind "volume_claim") }}
- name: {{ .Values.artifactsStore.name }}
{{- if eq .Values.artifactsStore.kind "volume_claim" }}
  persistentVolumeClaim:
    claimName: {{ .Values.artifactsStore.schema.volumeClaim | quote }}
{{- else }}
  hostPath:
    path: {{ .Values.artifactsStore.schema.hostPath | quote }}
{{- end }} {{- /* end store check */ -}}
{{- end }}
{{- if .Values.artifactsStore.secret }}
{{- if .Values.artifactsStore.secret.mountPath }}
- name: {{ .Values.artifactsStore.secret.name | quote }}
  secret:
    secretName: {{ .Values.artifactsStore.secret.name | quote }}
{{- end }}
{{- end }}
{{- if .Values.artifactsStore.configMap }}
{{- if .Values.artifactsStore.configMap.mountPath }}
- name: {{ .Values.artifactsStore.configMap.name | quote }}
  configMap:
    name: {{ .Values.artifactsStore.configMap.name | quote }}
{{- end }}
{{- end }}
{{- end }} {{- /* endif artifactsStore */ -}}
{{- end -}}  {{- /* end def artifactsStore volume mounts */ -}}
