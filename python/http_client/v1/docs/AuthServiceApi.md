# polyaxon_sdk.AuthServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**login**](AuthServiceApi.md#login) | **GET** /api/v1/users/token | List runs


# **login**
> V1Auth login(user=user, password=password)

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
api_instance = polyaxon_sdk.AuthServiceApi(polyaxon_sdk.ApiClient(configuration))
user = 'user_example' # str | User email. (optional)
password = 'password_example' # str | Project where the experiement will be assigned. (optional)

try:
    # List runs
    api_response = api_instance.login(user=user, password=password)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthServiceApi->login: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| User email. | [optional] 
 **password** | **str**| Project where the experiement will be assigned. | [optional] 

### Return type

[**V1Auth**](V1Auth.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

