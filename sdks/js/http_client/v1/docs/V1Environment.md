# PolyaxonSdk.V1Environment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**labels** | **{String: String}** |  | [optional] 
**annotations** | **{String: String}** |  | [optional] 
**node_selector** | **{String: String}** |  | [optional] 
**affinity** | [**V1Affinity**](V1Affinity.md) | Optional Affinity sets the scheduling constraints. | [optional] 
**tolerations** | [**[V1Toleration]**](V1Toleration.md) | Optional Tolerations to apply. | [optional] 
**node_name** | **String** | Optional NodeName is a request to schedule this pod onto a specific node. If it is non-empty, the scheduler simply schedules this pod onto that node, assuming that it fits resource requirements. | [optional] 
**service_account_name** | **String** |  | [optional] 
**host_aliases** | [**[V1HostAlias]**](V1HostAlias.md) | Optional HostAliases is an optional list of hosts and IPs that will be injected into the pod spec. | [optional] 
**security_context** | [**V1PodSecurityContext**](V1PodSecurityContext.md) | PodSecurityContext holds pod-level security attributes and common container settings. Some fields are also present in container.securityContext.  Field values of container.securityContext take precedence over field values of PodSecurityContext. | [optional] 
**image_pull_secrets** | **[String]** |  | [optional] 
**host_network** | **Boolean** | Host networking requested for this workflow pod. Default to false. | [optional] 
**dns_policy** | **String** | Set DNS policy for the pod. Defaults to \"ClusterFirst\". Valid values are 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'. DNS parameters given in DNSConfig will be merged with the policy selected with DNSPolicy. To have DNS options set along with hostNetwork, you have to specify DNS policy explicitly to 'ClusterFirstWithHostNet'. | [optional] 
**dns_config** | [**V1PodDNSConfig**](V1PodDNSConfig.md) | PodDNSConfig defines the DNS parameters of a pod in addition to those generated from DNSPolicy. | [optional] 
**scheduler_name** | **String** |  | [optional] 
**priority_class_name** | **String** | If specified, indicates the pod's priority. \"system-node-critical\" and \"system-cluster-critical\" are two special keywords which indicate the highest priorities with the former being the highest priority. Any other name must be defined by creating a PriorityClass object with that name. If not specified, the pod priority will be default or zero if there is no default. | [optional] 
**priority** | **Number** | The priority value. Various system components use this field to find the priority of the pod. When Priority Admission Controller is enabled, it prevents users from setting this field. The admission controller populates this field from PriorityClassName. The higher the value, the higher the priority. | [optional] 
**restart_policy** | **String** |  | [optional] 


