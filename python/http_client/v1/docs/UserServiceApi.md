# polyaxon_sdk.UserServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user**](UserServiceApi.md#get_user) | **GET** /api/v1/users | List runs


# **get_user**
> V1User get_user()

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
api_instance = polyaxon_sdk.UserServiceApi(polyaxon_sdk.ApiClient(configuration))

try:
    # List runs
    api_response = api_instance.get_user()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserServiceApi->get_user: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1User**](V1User.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

