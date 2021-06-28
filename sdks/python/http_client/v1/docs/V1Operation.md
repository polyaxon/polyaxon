# V1Operation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **float** |  | [optional] 
**kind** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**tags** | **list[str]** |  | [optional] 
**presets** | **list[str]** |  | [optional] 
**queue** | **str** |  | [optional] 
**cache** | [**V1Cache**](V1Cache.md) |  | [optional] 
**termination** | [**V1Termination**](V1Termination.md) |  | [optional] 
**plugins** | [**V1Plugins**](V1Plugins.md) |  | [optional] 
**schedule** | [**object**](.md) |  | [optional] 
**events** | [**list[V1EventTrigger]**](V1EventTrigger.md) |  | [optional] 
**hooks** | [**list[V1Hook]**](V1Hook.md) |  | [optional] 
**dependencies** | **list[str]** |  | [optional] 
**trigger** | [**V1TriggerPolicy**](V1TriggerPolicy.md) |  | [optional] 
**conditions** | **str** |  | [optional] 
**skip_on_upstream_skip** | **bool** |  | [optional] 
**matrix** | [**object**](.md) |  | [optional] 
**joins** | [**dict(str, V1Join)**](V1Join.md) |  | [optional] 
**params** | [**dict(str, V1Param)**](V1Param.md) |  | [optional] 
**run_patch** | [**object**](.md) |  | [optional] 
**patch_strategy** | [**V1PatchStrategy**](V1PatchStrategy.md) |  | [optional] 
**is_preset** | **bool** |  | [optional] 
**is_approved** | **bool** |  | [optional] 
**template** | [**V1Template**](V1Template.md) |  | [optional] 
**build** | [**V1Build**](V1Build.md) |  | [optional] 
**cost** | **float** |  | [optional] 
**path_ref** | **str** |  | [optional] 
**hub_ref** | **str** |  | [optional] 
**dag_ref** | **str** |  | [optional] 
**url_ref** | **str** |  | [optional] 
**component** | [**V1Component**](V1Component.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


