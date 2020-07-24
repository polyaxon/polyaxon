# V1Environment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**labels** | **dict(str, str)** |  | [optional] 
**annotations** | **dict(str, str)** |  | [optional] 
**node_selector** | **dict(str, str)** |  | [optional] 
**affinity** | [**V1Affinity**](V1Affinity.md) |  | [optional] 
**tolerations** | [**list[V1Toleration]**](V1Toleration.md) | Optional Tolerations to apply. | [optional] 
**node_name** | **str** | Optional NodeName is a request to schedule this pod onto a specific node. If it is non-empty, the scheduler simply schedules this pod onto that node, assuming that it fits resource requirements. | [optional] 
**service_account_name** | **str** |  | [optional] 
**host_aliases** | [**list[V1HostAlias]**](V1HostAlias.md) | Optional HostAliases is an optional list of hosts and IPs that will be injected into the pod spec. | [optional] 
**security_context** | [**V1PodSecurityContext**](V1PodSecurityContext.md) |  | [optional] 
**image_pull_secrets** | **list[str]** |  | [optional] 
**host_network** | **bool** | Host networking requested for this workflow pod. Default to false. | [optional] 
**host_pid** | **str** | Use the host&#39;s pid namespace. Default to false. | [optional] 
**dns_policy** | **str** | Set DNS policy for the pod. Defaults to \&quot;ClusterFirst\&quot;. Valid values are &#39;ClusterFirstWithHostNet&#39;, &#39;ClusterFirst&#39;, &#39;Default&#39; or &#39;None&#39;. DNS parameters given in DNSConfig will be merged with the policy selected with DNSPolicy. To have DNS options set along with hostNetwork, you have to specify DNS policy explicitly to &#39;ClusterFirstWithHostNet&#39;. | [optional] 
**dns_config** | [**V1PodDNSConfig**](V1PodDNSConfig.md) |  | [optional] 
**scheduler_name** | **str** |  | [optional] 
**priority_class_name** | **str** | If specified, indicates the pod&#39;s priority. \&quot;system-node-critical\&quot; and \&quot;system-cluster-critical\&quot; are two special keywords which indicate the highest priorities with the former being the highest priority. Any other name must be defined by creating a PriorityClass object with that name. If not specified, the pod priority will be default or zero if there is no default. | [optional] 
**priority** | **int** | The priority value. Various system components use this field to find the priority of the pod. When Priority Admission Controller is enabled, it prevents users from setting this field. The admission controller populates this field from PriorityClassName. The higher the value, the higher the priority. | [optional] 
**restart_policy** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


