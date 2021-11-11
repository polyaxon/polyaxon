# V1Dask


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **str** |  | [optional] [default to 'dask']
**threads** | **int** |  | [optional] 
**scale** | **int** |  | [optional] 
**adapt_min** | **int** |  | [optional] 
**adapt_max** | **int** |  | [optional] 
**adapt_interval** | **str** |  | [optional] 
**environment** | [**V1Environment**](V1Environment.md) |  | [optional] 
**connections** | **list[str]** |  | [optional] 
**volumes** | [**list[V1Volume]**](V1Volume.md) | Volumes is a list of volumes that can be mounted. | [optional] 
**init** | [**list[V1Init]**](V1Init.md) |  | [optional] 
**sidecars** | [**list[V1Container]**](V1Container.md) |  | [optional] 
**container** | [**V1Container**](V1Container.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


