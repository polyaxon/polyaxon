interface EnabledInterface {
  enabled: boolean;
}

interface ResourceDefInteface {
  cpu: string;
  memory: string;
}

interface ResourcesInterface {
  limits: ResourceDefInteface;
  requests: ResourceDefInteface;
}

interface TlsInterface extends EnabledInterface{
  hosts: string[];
  secretName: string;
}

interface IngressInterface extends EnabledInterface {
  annotations: {[key: string]: string};
  resources: ResourcesInterface;
  tls: TlsInterface;
}

interface UserInterface {
  username: string;
  email: string;
  password: string;
}

interface PersistenceDefInterface {
  existingClaim: string;
  mountPath: string;
  hostPath: string;
  readonly: boolean;
}

interface PersistenceInterface {
  logs: PersistenceDefInterface;
  repos: PersistenceDefInterface;
  upload: PersistenceDefInterface;
  data: {[key: string]: PersistenceDefInterface};
  outputs: {[key: string]: PersistenceDefInterface};
}

interface LDAPInterface extends EnabledInterface {
  serverUri: string;
  globalOptions: {[key: string]: string};
  connectionOptions: {[key: string]: string};
  bindDN: string;
  bindPassword: string;
  userSearchBaseDN: string;
  userSearchFilterStr: string;
  userDNTemplate: string;
  startTLS: boolean;
  userAttrMap: {[key: string]: string};
  groupSearchBaseDN: string;
  groupSearchGroupType: string;
  requireGroup: string;
  denyGroup: string;
}

interface SSODefInterface extends EnabledInterface {
  clientId: string;
  clientSecret: string;
}

interface GitlabInterface extends SSODefInterface {
  url: string;
}

interface AzureInterface extends SSODefInterface {
  tenantId: string;
}

interface AuthInterface {
  ldap: LDAPInterface;
  github: SSODefInterface;
  bitbucket: SSODefInterface;
  gitlab: GitlabInterface;
  azure: AzureInterface;
}

interface NodeSelectorsInterface {
  core: {[key: string]: string};
  experiments: {[key: string]: string};
  jobs: {[key: string]: string};
  builds: {[key: string]: string};
}

interface AffinityInterface {
  core: {[key: string]: string};
  experiments: {[key: string]: string};
  jobs: {[key: string]: string};
  builds: {[key: string]: string};
}

interface TolerationsInterface {
  resourcesDaemon: Array<{[key: string]: string}>;
  core: Array<{[key: string]: string}>;
  experiments: Array<{[key: string]: string}>;
  jobs: Array<{[key: string]: string}>;
  builds: Array<{[key: string]: string}>;
}

interface ServiceInterface {
  replicas: number;
  resources: ResourcesInterface;
}

interface EmailInterface {
  host: string;
  port: number;
  useTls: boolean;
  hostUser: string;
  hostPassword: string;
}

interface WebHook {
  url: string;
  method: string;
  channel: string;
  roomid: string;
}

interface IntegrationsInterface {
  slack: WebHook[];
  hipchat: WebHook[];
  mattermost: WebHook[];
  discord: WebHook[];
  pagerduty: WebHook[];
  webhooks: WebHook[];
}

export interface ConfigInterface {
  rbac?: EnabledInterface;
  ingress?: IngressInterface;
  serviceType?: 'ClusterIP' | 'LoadBalancer' | 'NodePort';
  limitResources?: boolean;
  user?: UserInterface;
  passwordLenght?:  number;
  timeZone?: string;
  persistence?: PersistenceInterface;
  auth?: AuthInterface;
  nodeSelectors?: NodeSelectorsInterface;
  affinity?: AffinityInterface;
  tolerations?: TolerationsInterface;
  api?: ServiceInterface;
  scheduler?: ServiceInterface;
  hpsearch?: ServiceInterface;
  eventsHandlers?: ServiceInterface;
  eventMonitors?: ServiceInterface;
  email?: EmailInterface;
  integrations?: IntegrationsInterface;
  privateRegistries?: string[];
}
