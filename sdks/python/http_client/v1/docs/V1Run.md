# V1Run

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**tags** | **list[str]** |  | [optional] 
**user** | **str** |  | [optional] 
**owner** | **str** |  | [optional] 
**project** | **str** |  | [optional] 
**schedule_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**wait_time** | **int** |  | [optional] 
**duration** | **int** |  | [optional] 
**is_managed** | **bool** |  | [optional] 
**is_approved** | **bool** |  | [optional] 
**pending** | [**V1RunPending**](V1RunPending.md) |  | [optional] 
**content** | **str** |  | [optional] 
**raw_content** | **str** |  | [optional] 
**status** | [**V1Statuses**](V1Statuses.md) |  | [optional] 
**bookmarked** | **bool** |  | [optional] 
**live_state** | **int** |  | [optional] 
**readme** | **str** |  | [optional] 
**meta_info** | [**object**](.md) |  | [optional] 
**kind** | [**V1RunKind**](V1RunKind.md) |  | [optional] 
**runtime** | [**V1RunKind**](V1RunKind.md) |  | [optional] 
**inputs** | [**object**](.md) |  | [optional] 
**outputs** | [**object**](.md) |  | [optional] 
**original** | [**V1Cloning**](V1Cloning.md) |  | [optional] 
**pipeline** | [**V1Pipeline**](V1Pipeline.md) |  | [optional] 
**status_conditions** | [**list[V1StatusCondition]**](V1StatusCondition.md) |  | [optional] 
**role** | **str** |  | [optional] 
**settings** | [**V1RunSettings**](V1RunSettings.md) |  | [optional] 
**graph** | [**object**](.md) |  | [optional] 
**merge** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


