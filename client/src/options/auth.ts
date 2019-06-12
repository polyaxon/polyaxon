import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const AUTH_AZURE_ENABLED =
  `${option_namespaces.AUTH_AZURE}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.ENABLED}`;
export const AUTH_AZURE_VERIFICATION_SCHEDULE =
  `${option_namespaces.AUTH_AZURE}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.VERIFICATION_SCHEDULE}`;
export const AUTH_AZURE_TENANT_ID =
  `${option_namespaces.AUTH_AZURE}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.TENANT_ID }`;
export const AUTH_AZURE_CLIENT_ID =
  `${option_namespaces.AUTH_AZURE}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CLIENT_ID}`;
export const AUTH_AZURE_CLIENT_SECRET =
  `${option_namespaces.AUTH_AZURE}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CLIENT_SECRET}`;

export const AUTH_AZURE_KEYS = [
  AUTH_AZURE_ENABLED,
  AUTH_AZURE_VERIFICATION_SCHEDULE,
  AUTH_AZURE_TENANT_ID,
  AUTH_AZURE_CLIENT_ID,
  AUTH_AZURE_CLIENT_SECRET,
];

export const AUTH_BITBUCKET_ENABLED =
  `${option_namespaces.AUTH_BITBUCKET}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.ENABLED}`;
export const AUTH_BITBUCKET_VERIFICATION_SCHEDULE =
  `${option_namespaces.AUTH_BITBUCKET}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.VERIFICATION_SCHEDULE}`;
export const AUTH_BITBUCKET_CLIENT_ID =
  `${option_namespaces.AUTH_BITBUCKET}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CLIENT_ID}`;
export const AUTH_BITBUCKET_CLIENT_SECRET =
  `${option_namespaces.AUTH_BITBUCKET}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CLIENT_SECRET}`;

export const AUTH_BITBUCKET_KEYS = [
  AUTH_BITBUCKET_ENABLED,
  AUTH_BITBUCKET_VERIFICATION_SCHEDULE,
  AUTH_BITBUCKET_CLIENT_ID,
  AUTH_BITBUCKET_CLIENT_SECRET,
];

export const AUTH_GITHUB_ENABLED =
  `${option_namespaces.AUTH_GITHUB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.ENABLED}`;
export const AUTH_GITHUB_VERIFICATION_SCHEDULE =
  `${option_namespaces.AUTH_GITHUB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.VERIFICATION_SCHEDULE}`;
export const AUTH_GITHUB_CLIENT_ID =
  `${option_namespaces.AUTH_GITHUB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CLIENT_ID}`;
export const AUTH_GITHUB_CLIENT_SECRET =
  `${option_namespaces.AUTH_GITHUB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CLIENT_SECRET}`;

export const AUTH_GITHUB_KEYS = [
  AUTH_GITHUB_ENABLED,
  AUTH_GITHUB_VERIFICATION_SCHEDULE,
  AUTH_GITHUB_CLIENT_ID,
  AUTH_GITHUB_CLIENT_SECRET,
];

export const AUTH_GITLAB_ENABLED =
  `${option_namespaces.AUTH_GITLAB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.ENABLED}`;
export const AUTH_GITLAB_VERIFICATION_SCHEDULE =
  `${option_namespaces.AUTH_GITLAB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.VERIFICATION_SCHEDULE}`;
export const AUTH_GITLAB_CLIENT_ID =
  `${option_namespaces.AUTH_GITLAB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CLIENT_ID}`;
export const AUTH_GITLAB_CLIENT_SECRET =
  `${option_namespaces.AUTH_GITLAB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.CLIENT_SECRET}`;
export const AUTH_GITLAB_URL =
  `${option_namespaces.AUTH_GITLAB}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.URL}`;

export const AUTH_GITLAB_KEYS = [
  AUTH_GITLAB_ENABLED,
  AUTH_GITLAB_VERIFICATION_SCHEDULE,
  AUTH_GITLAB_CLIENT_ID,
  AUTH_GITLAB_CLIENT_SECRET,
  AUTH_GITLAB_URL,
];
