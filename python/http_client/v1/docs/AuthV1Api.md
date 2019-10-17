# polyaxon_sdk.AuthV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**login**](AuthV1Api.md#login) | **POST** /api/v1/users/token | List runs


# **login**
> V1Auth login(body)

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
api_instance = polyaxon_sdk.AuthV1Api(polyaxon_sdk.ApiClient(configuration))
body = polyaxon_sdk.V1CredsBodyRequest() # V1CredsBodyRequest | 

try:
    # List runs
    api_response = api_instance.login(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthV1Api->login: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**V1CredsBodyRequest**](V1CredsBodyRequest.md)|  | 

### Return type

[**V1Auth**](V1Auth.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

