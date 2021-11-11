

# V1DiffStoppingPolicy

Early stopping with diff factor stopping, this policy computes checks runs against the best run and stops those whose performance is worse than the best by the factor defined by the user.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  |  [optional]
**percent** | **Float** |  |  [optional]
**evaluationInterval** | **Integer** | Interval/Frequency for applying the policy. |  [optional]
**minInterval** | **Integer** |  |  [optional]
**minSamples** | **Integer** |  |  [optional]



