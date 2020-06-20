# polyaxon_sdk.ArtifactsStoresV1Api
Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**upload_artifact**](ArtifactsStoresV1Api.md#upload_artifact) | **POST** /api/v1/catalogs/{owner}/artifacts/{uuid}/upload | Upload artifact to a store


# **upload_artifact**
> upload_artifact(owner, uuid, uploadfile, path=path, overwrite=overwrite)

Upload artifact to a store

### Example

* Api Key Authentication (ApiKey):
```python
from __future__ import print_function
import time
import polyaxon_sdk
from polyaxon_sdk.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration = polyaxon_sdk.Configuration(
    host = "http://localhost",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Enter a context with an instance of the API client
with polyaxon_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = polyaxon_sdk.ArtifactsStoresV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Unique integer identifier of the entity
uploadfile = '/path/to/file' # file | The file to upload.
path = 'path_example' # str | File path query params. (optional)
overwrite = True # bool | File path query params. (optional)

    try:
        # Upload artifact to a store
        api_instance.upload_artifact(owner, uuid, uploadfile, path=path, overwrite=overwrite)
    except ApiException as e:
        print("Exception when calling ArtifactsStoresV1Api->upload_artifact: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **uploadfile** | **file**| The file to upload. | 
 **path** | **str**| File path query params. | [optional] 
 **overwrite** | **bool**| File path query params. | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

