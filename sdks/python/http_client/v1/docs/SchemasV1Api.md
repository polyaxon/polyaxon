# polyaxon_sdk.SchemasV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**schemas_v1_no_op**](SchemasV1Api.md#schemas_v1_no_op) | **GET** /schemas | List teams names


# **schemas_v1_no_op**
> V1Schemas schemas_v1_no_op()

List teams names

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
api_instance = polyaxon_sdk.SchemasV1Api(polyaxon_sdk.ApiClient(configuration))

try:
    # List teams names
    api_response = api_instance.schemas_v1_no_op()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SchemasV1Api->schemas_v1_no_op: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1Schemas**](V1Schemas.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

