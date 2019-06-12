import * as option_namespaces from './namespaces';
import * as separators from './separators';
import * as option_subjects from './subjects';

export const INTEGRATIONS_WEBHOOKS_DISCORD =
  `${option_namespaces.INTEGRATIONS_WEBHOOKS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.DISCORD}`;
export const INTEGRATIONS_WEBHOOKS_HIPCHAT =
  `${option_namespaces.INTEGRATIONS_WEBHOOKS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.HIPCHAT}`;
export const INTEGRATIONS_WEBHOOKS_MATTERMOST =
  `${option_namespaces.INTEGRATIONS_WEBHOOKS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.MATTERMOST}`;
export const INTEGRATIONS_WEBHOOKS_PAGER_DUTY =
  `${option_namespaces.INTEGRATIONS_WEBHOOKS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.PAGER_DUTY}`;
export const INTEGRATIONS_WEBHOOKS_SLACK =
  `${option_namespaces.INTEGRATIONS_WEBHOOKS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.SLACK}`;
export const INTEGRATIONS_WEBHOOKS_GENERIC =
  `${option_namespaces.INTEGRATIONS_WEBHOOKS}${separators.NAMESPACE_DB_OPTION_MARKER}${option_subjects.GENERIC}`;

export const INTEGRATIONS_KEYS = [
  INTEGRATIONS_WEBHOOKS_DISCORD,
  INTEGRATIONS_WEBHOOKS_HIPCHAT,
  INTEGRATIONS_WEBHOOKS_MATTERMOST,
  INTEGRATIONS_WEBHOOKS_PAGER_DUTY,
  INTEGRATIONS_WEBHOOKS_SLACK,
  INTEGRATIONS_WEBHOOKS_GENERIC,
];
