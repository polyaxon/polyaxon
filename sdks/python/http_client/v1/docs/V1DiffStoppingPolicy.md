# V1DiffStoppingPolicy

Early stopping with diff factor stopping, this policy computes checks runs against the best run and stops those whose performance is worse than the best by the factor defined by the user.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **str** |  | [optional] 
**percent** | **float** |  | [optional] 
**evaluation_interval** | **int** | Interval/Frequency for applying the policy. | [optional] 
**min_interval** | **int** |  | [optional] 
**min_samples** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


