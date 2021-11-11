

# V1MedianStoppingPolicy

Early stopping with median stopping, this policy computes running medians across all runs and stops those whose best performance is worse than the median of the running runs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  |  [optional]
**evaluationInterval** | **Integer** | Interval/Frequency for applying the policy. |  [optional]
**minInterval** | **Integer** |  |  [optional]
**minSamples** | **Integer** |  |  [optional]



