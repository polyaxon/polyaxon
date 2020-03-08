{{- /*
Config artifacts store secrets/configmap
*/}}
{{- define "config.artifactsStore.envFrom" -}}
{{- if and .Values.artifactsStore .Values.artifactsStore.secret }}
- secretRef:
    name: {{ .Values.artifactsStore.secret.name | quote }}
{{- end }} {{- /* endif */ -}}
{{- if and .Values.artifactsStore .Values.artifactsStore.configMap }}
- configMapRef:
    name: {{ .Values.artifactsStore.configMap.name | quote }}
{{- end }} {{- /* endif */ -}}
{{- end -}}

{{- define "config.artifactsStore.mount" -}}
{{- if and .Values.artifactsStore (or (eq .Values.artifactsStore.kind "host_path") (eq .Values.artifactsStore.kind "volume_claim")) }}
- mountPath: {{ .Values.artifactsStore.schema.mountPath | quote }}
  name: {{ .Values.artifactsStore.name }}
  {{ if .Values.artifactsStore.schema.subPath -}}
  subPath: {{ .Values.artifactsStore.schema.subPath | quote }}
  {{- end }}
{{- end }}
{{- end -}}  {{- /* end def artifactsStore volume mounts */ -}}

{{- define "config.artifactsStore.volume" -}}
{{- if and .Values.artifactsStore (or (eq .Values.artifactsStore.kind "host_path") (eq .Values.artifactsStore.kind "volume_claim")) }}
- name: {{ .Values.artifactsStore.name }}
{{- if eq .Values.artifactsStore.kind "volume_claim" }}
  persistentVolumeClaim:
    claimName: {{ .Values.artifactsStore.schema.volumeClaim | quote }}
{{- else }}
  hostPath:
    path: {{ .Values.artifactsStore.schema.hostPath | quote }}
{{- end }} {{- /* end store check */ -}}
{{- end }}
{{- end -}}  {{- /* end def artifactsStore volume mounts */ -}}
