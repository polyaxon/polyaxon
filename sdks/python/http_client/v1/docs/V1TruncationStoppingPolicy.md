# V1TruncationStoppingPolicy

Early stopping with truncation stopping, this policy stops a percentage of all running runs at every evaluation.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **str** |  | [optional] [default to 'truncation']
**percent** | **int** | The percentage of runs to stop, at each evaluation interval. e.g. 1 - 99. | [optional] 
**evaluation_interval** | **int** | Interval/Frequency for applying the policy. | [optional] 
**min_interval** | **int** |  | [optional] 
**min_samples** | **int** |  | [optional] 
**include_succeeded** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


