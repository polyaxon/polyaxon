{{/*
Auth
*/}}
{{- define "config.auth" }}
{{- if .Values.auth.ldap.enabled }}
- name: POLYAXON_AUTH_LDAP
  value: "true"
- name: POLYAXON_AUTH_LDAP_SERVER_URI
  value: {{ .Values.auth.ldap.serverUri | quote }}
- name: POLYAXON_AUTH_LDAP_GLOBAL_OPTIONS
  value: {{ toJson .Values.auth.ldap.globalOptions | quote }}
- name: POLYAXON_AUTH_LDAP_CONNECTION_OPTIONS
  value: {{ toJson .Values.auth.ldap.connectionOptions | quote }}
- name: POLYAXON_AUTH_LDAP_BIND_DN
  value: {{ .Values.auth.ldap.bindDN | quote }}
- name: POLYAXON_AUTH_LDAP_BIND_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-ldap-bind-password
- name: POLYAXON_AUTH_LDAP_USER_SEARCH_BASE_DN
  value: {{ .Values.auth.ldap.userSearchBaseDN | quote }}
- name: POLYAXON_AUTH_LDAP_USER_SEARCH_FILTERSTR
  value: {{ .Values.auth.ldap.userSearchFilterStr | quote }}
- name: POLYAXON_AUTH_LDAP_USER_DN_TEMPLATE
  value: {{ .Values.auth.ldap.userDNTemplate | quote }}
- name: POLYAXON_AUTH_LDAP_START_TLS
  value: {{ .Values.auth.ldap.startTLS | quote }}
- name: POLYAXON_AUTH_LDAP_USER_ATTR_MAP
  value: {{ toJson .Values.auth.ldap.userAttrMap | quote }}
- name: POLYAXON_AUTH_LDAP_GROUP_SEARCH_BASE_DN
  value: {{ .Values.auth.ldap.groupSearchBaseDN | quote }}
- name: POLYAXON_AUTH_LDAP_GROUP_SEARCH_GROUP_TYPE
  value: {{ .Values.auth.ldap.groupSearchGroupType | quote }}
{{- if .Values.auth.ldap.requireGroup }}
- name: POLYAXON_AUTH_LDAP_REQUIRE_GROUP
  value: {{ .Values.auth.ldap.requireGroup | quote }}
{{- end }}
{{- if .Values.auth.ldap.denyGroup }}
- name: POLYAXON_AUTH_LDAP_DENY_GROUP
  value: {{ .Values.auth.ldap.denyGroup | quote }}
{{- end }}
{{- end }}
{{- if .Values.auth.github.enabled }}
- name: POLYAXON_AUTH_GITHUB
  value: "true"
- name: POLYAXON_AUTH_GITHUB_CLIENT_ID
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-github-client-id
- name: POLYAXON_AUTH_GITHUB_CLIENT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-github-client-secret
{{- end }}
{{- if .Values.auth.bitbucket.enabled }}
- name: POLYAXON_AUTH_BITBUCKET
  value: "true"
- name: POLYAXON_AUTH_BITBUCKET_CLIENT_ID
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-bitbucket-client-id
- name: POLYAXON_AUTH_BITBUCKET_CLIENT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-bitbucket-client-secret
{{- end }}
{{- if .Values.auth.gitlab.enabled }}
- name: POLYAXON_AUTH_GITLAB
  value: "true"
- name: POLYAXON_AUTH_GITLAB_URL
  value: {{ .Values.auth.gitlab.url | quote }}
- name: POLYAXON_AUTH_GITLAB_CLIENT_ID
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-gitlab-client-id
- name: POLYAXON_AUTH_GITLAB_CLIENT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-gitlab-client-secret
{{- end }}
{{- end -}}
