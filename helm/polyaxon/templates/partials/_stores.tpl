{{- /*
Config artifacts store secrets/configmap
*/}}
{{- define "config.artifactsStore.envFrom" -}}
{{- if and .Values.artifactsStore .Values.artifactsStore.secret (empty .Values.artifactsStore.secret.mountPath) }}
- secretRef:
    name: {{ .Values.artifactsStore.secret.name | quote }}
{{- end }} {{- /* endif */ -}}
{{- if and .Values.artifactsStore .Values.artifactsStore.configMap (empty .Values.artifactsStore.configMap.mountPath) }}
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
{{- if and .Values.artifactsStore .Values.artifactsStore.secret .Values.artifactsStore.secret.mountPath }}
- mountPath: {{ .Values.artifactsStore.secret.mountPath | quote }}
  name: {{ .Values.artifactsStore.secret.name | quote }}
  readOnly: true
{{- end }}
{{- if and .Values.artifactsStore .Values.artifactsStore.configMap .Values.artifactsStore.configMap.mountPath }}
- mountPath: {{ .Values.artifactsStore.configMap.mountPath | quote }}
  name: {{ .Values.artifactsStore.configMap.name | quote }}
  readOnly: true
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
{{- if and .Values.artifactsStore .Values.artifactsStore.secret .Values.artifactsStore.secret.mountPath }}
- name: {{ .Values.artifactsStore.secret.name | quote }}
  secret:
    secretName: {{ .Values.artifactsStore.secret.name | quote }}
{{- end }}
{{- if and .Values.artifactsStore .Values.artifactsStore.configMap .Values.artifactsStore.configMap.mountPath }}
- name: {{ .Values.artifactsStore.configMap.name | quote }}
  configMap:
    name: {{ .Values.artifactsStore.configMap.name | quote }}
{{- end }}
{{- end -}}  {{- /* end def artifactsStore volume mounts */ -}}
