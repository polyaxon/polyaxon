export interface EnabledInterface {
  enabled: boolean;
}

export interface ResourceDefInterface {
  cpu: string;
  memory: string;
}

export interface ResourcesInterface {
  limits: ResourceDefInterface;
  requests: ResourceDefInterface;
}

export interface TlsInterface extends EnabledInterface {
  hosts: string[];
  secretName: string;
}

export interface IngressInterface extends EnabledInterface {
  annotations: {[key: string]: string};
  resources: ResourcesInterface;
  tls: TlsInterface;
}

export interface UserInterface {
  username: string;
  email: string;
  password: string;
}

export interface PersistenceDefInterface {
  existingClaim?: string;
  mountPath?: string;
  hostPath?: string;
  readonly?: boolean;
}

export interface PersistenceInterface {
  logs: PersistenceDefInterface;
  repos: PersistenceDefInterface;
  upload: PersistenceDefInterface;
  data: {[key: string]: PersistenceDefInterface};
  outputs: {[key: string]: PersistenceDefInterface};
}

export interface LDAPInterface extends EnabledInterface {
  serverUri: string;
  globalOptions: string;
  connectionOptions: string;
  bindDN: string;
  bindPassword: string;
  userSearchBaseDN: string;
  userSearchFilterStr: string;
  userDNTemplate: string;
  startTLS: boolean;
  userAttrMap: string;
  groupSearchBaseDN: string;
  groupSearchGroupType: string;
  requireGroup: string;
  denyGroup: string;
}

export interface SSODefInterface extends EnabledInterface {
  clientId: string;
  clientSecret: string;
}

export interface GitlabInterface extends SSODefInterface {
  url: string;
}

export interface AzureInterface extends SSODefInterface {
  tenantId: string;
}

export interface AuthInterface {
  ldap?: LDAPInterface;
  github?: SSODefInterface;
  bitbucket?: SSODefInterface;
  gitlab?: GitlabInterface;
  azure?: AzureInterface;
}

export interface NodeSelectorsStrInterface {
  core: string;
  experiments: string;
  jobs: string;
  builds: string;
}

export interface AffinityStrInterface {
  core: string;
  experiments: string;
  jobs: string;
  builds: string;
}

export interface TolerationsStrInterface {
  resourcesDaemon: string;
  core: string;
  experiments: string;
  jobs: string;
  builds: string;
}

export interface NodeSelectorsInterface {
  core: {[key: string]: string};
  experiments: {[key: string]: string};
  jobs: {[key: string]: string};
  builds: {[key: string]: string};
}

export interface AffinityInterface {
  core: {[key: string]: string};
  experiments: {[key: string]: string};
  jobs: {[key: string]: string};
  builds: {[key: string]: string};
}

export interface TolerationsInterface {
  resourcesDaemon: Array<{[key: string]: string}>;
  core: Array<{[key: string]: string}>;
  experiments: Array<{[key: string]: string}>;
  jobs: Array<{[key: string]: string}>;
  builds: Array<{[key: string]: string}>;
}


export interface ServiceInterface {
  replicas: number;
  resources: ResourcesInterface;
}

export interface EmailInterface {
  host: string;
  port: number;
  useTls: boolean;
  hostUser: string;
  hostPassword: string;
}

export interface WebHook {
  url: string;
  method: string;
  channel: string;
  roomid: string;
}

export interface IntegrationsStrInterface {
  slack: string;
  hipchat: string;
  mattermost: string;
  discord: string;
  pagerduty: string;
  webhooks: string;
}

export interface IntegrationsInterface {
  slack: WebHook[];
  hipchat: WebHook[];
  mattermost: WebHook[];
  discord: WebHook[];
  pagerduty: WebHook[];
  webhooks: WebHook[];
}

export interface PostgresPersistenceInterface {
  enabled: boolean;
  size: string;
  existingClaim: string;
}

export interface PostgresInterface {
  enabled: boolean;
  postgresUser: string;
  postgresPassword: string;
  postgresDatabase: string;
  externalPostgresHost: string;
  persistence: PostgresPersistenceInterface;
}

export type SERVICE_TYPES = 'ClusterIP' | 'LoadBalancer' | 'NodePort';

export interface ConfigInterface {
  namespace?: string;
  rbac?: EnabledInterface;
  ingress?: IngressInterface;
  serviceType?: SERVICE_TYPES;
  limitResources?: boolean;
  user?: UserInterface;
  passwordLength?:  number;
  timeZone?: string;
  persistence?: PersistenceInterface;
  defaultPersistence?: PersistenceInterface;
  auth?: AuthInterface;
  nodeSelectorsStr?: NodeSelectorsStrInterface;
  affinityStr?: AffinityStrInterface;
  tolerationsStr?: TolerationsStrInterface;
  nodeSelectors?: NodeSelectorsInterface;
  affinity?: AffinityInterface;
  tolerations?: TolerationsInterface;
  api?: ServiceInterface;
  scheduler?: ServiceInterface;
  hpsearch?: ServiceInterface;
  eventsHandlers?: ServiceInterface;
  eventMonitors?: ServiceInterface;
  email?: EmailInterface;
  integrationsStr?: IntegrationsStrInterface;
  integrations?: IntegrationsInterface;
  privateRegistries?: string[];
  privateRegistriesStr?: string;
  postgresql?: PostgresInterface;
}
