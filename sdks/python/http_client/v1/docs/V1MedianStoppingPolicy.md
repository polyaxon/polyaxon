# V1MedianStoppingPolicy

Early stopping with median stopping, this policy computes running medians across all runs and stops those whose best performance is worse than the median of the running runs.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **str** |  | [optional] [default to 'median']
**evaluation_interval** | **int** | Interval/Frequency for applying the policy. | [optional] 
**min_interval** | **int** |  | [optional] 
**min_samples** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


