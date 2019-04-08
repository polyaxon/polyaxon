{{- /*
Config securityContext with static GID
*/}}
{{- define "securityContext" -}}
securityContext:
  fsGroup: 2222
{{- end -}}
