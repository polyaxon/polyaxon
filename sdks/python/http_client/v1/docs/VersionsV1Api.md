# polyaxon_sdk.VersionsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**versions_v1_get_log_handler**](VersionsV1Api.md#versions_v1_get_log_handler) | **GET** /api/v1/log_handler | 
[**versions_v1_get_versions**](VersionsV1Api.md#versions_v1_get_versions) | **GET** /api/v1/version | Get current user


# **versions_v1_get_log_handler**
> V1LogHandler versions_v1_get_log_handler()



### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.VersionsV1Api(polyaxon_sdk.ApiClient(configuration))

try:
    api_response = api_instance.versions_v1_get_log_handler()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsV1Api->versions_v1_get_log_handler: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1LogHandler**](V1LogHandler.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **versions_v1_get_versions**
> V1Versions versions_v1_get_versions()

Get current user

### Example
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = polyaxon_sdk.VersionsV1Api(polyaxon_sdk.ApiClient(configuration))

try:
    # Get current user
    api_response = api_instance.versions_v1_get_versions()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionsV1Api->versions_v1_get_versions: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1Versions**](V1Versions.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

