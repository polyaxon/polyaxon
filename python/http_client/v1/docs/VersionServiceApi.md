# polyaxon_sdk.VersionServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_log_handler**](VersionServiceApi.md#get_log_handler) | **GET** /api/v1/log_handler | List bookmarked runs
[**get_versions**](VersionServiceApi.md#get_versions) | **GET** /api/v1/versions | List runs


# **get_log_handler**
> V1LogHandler get_log_handler()

List bookmarked runs

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
api_instance = polyaxon_sdk.VersionServiceApi(polyaxon_sdk.ApiClient(configuration))

try:
    # List bookmarked runs
    api_response = api_instance.get_log_handler()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionServiceApi->get_log_handler: %s\n" % e)
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

# **get_versions**
> V1Versions get_versions()

List runs

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
api_instance = polyaxon_sdk.VersionServiceApi(polyaxon_sdk.ApiClient(configuration))

try:
    # List runs
    api_response = api_instance.get_versions()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VersionServiceApi->get_versions: %s\n" % e)
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

