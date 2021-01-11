# PolyaxonSdk.V1Operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **Number** |  | [optional] 
**kind** | **String** |  | [optional] 
**name** | **String** |  | [optional] 
**description** | **String** |  | [optional] 
**tags** | **[String]** |  | [optional] 
**presets** | **[String]** |  | [optional] 
**queue** | **String** |  | [optional] 
**cache** | [**V1Cache**](V1Cache.md) |  | [optional] 
**termination** | [**V1Termination**](V1Termination.md) |  | [optional] 
**plugins** | [**V1Plugins**](V1Plugins.md) |  | [optional] 
**schedule** | [**Object**](.md) |  | [optional] 
**events** | [**[V1EventTrigger]**](V1EventTrigger.md) |  | [optional] 
**hooks** | [**[V1Hook]**](V1Hook.md) |  | [optional] 
**dependencies** | **[String]** |  | [optional] 
**trigger** | [**V1TriggerPolicy**](V1TriggerPolicy.md) |  | [optional] 
**conditions** | **[String]** |  | [optional] 
**skip_on_upstream_skip** | **Boolean** |  | [optional] 
**matrix** | [**Object**](.md) |  | [optional] 
**joins** | [**{String: V1Join}**](V1Join.md) |  | [optional] 
**params** | [**{String: V1Param}**](V1Param.md) |  | [optional] 
**run_patch** | [**Object**](.md) |  | [optional] 
**patch_strategy** | [**V1PatchStrategy**](V1PatchStrategy.md) |  | [optional] 
**is_preset** | **Boolean** |  | [optional] 
**is_approved** | **Boolean** |  | [optional] 
**template** | [**V1Template**](V1Template.md) |  | [optional] 
**url_ref** | **String** |  | [optional] 
**path_ref** | **String** |  | [optional] 
**hub_ref** | **String** |  | [optional] 
**dag_ref** | **String** |  | [optional] 
**component** | [**V1Component**](V1Component.md) |  | [optional] 


