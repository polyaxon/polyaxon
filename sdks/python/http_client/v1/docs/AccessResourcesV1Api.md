# polyaxon_sdk.AccessResourcesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**access_resources_v1_create_access_resource**](AccessResourcesV1Api.md#access_resources_v1_create_access_resource) | **POST** /api/v1/orgs/{owner}/access_resources | Create access resource
[**access_resources_v1_delete_access_resource**](AccessResourcesV1Api.md#access_resources_v1_delete_access_resource) | **DELETE** /api/v1/orgs/{owner}/access_resources/{uuid} | Delete access resource
[**access_resources_v1_get_access_resource**](AccessResourcesV1Api.md#access_resources_v1_get_access_resource) | **GET** /api/v1/orgs/{owner}/access_resources/{uuid} | Get access resource
[**access_resources_v1_list_access_resource_names**](AccessResourcesV1Api.md#access_resources_v1_list_access_resource_names) | **GET** /api/v1/orgs/{owner}/access_resources/names | List access resource names
[**access_resources_v1_list_access_resources**](AccessResourcesV1Api.md#access_resources_v1_list_access_resources) | **GET** /api/v1/orgs/{owner}/access_resources | List access resources
[**access_resources_v1_patch_access_resource**](AccessResourcesV1Api.md#access_resources_v1_patch_access_resource) | **PATCH** /api/v1/orgs/{owner}/access_resources/{access_resource.uuid} | Patch access resource
[**access_resources_v1_update_access_resource**](AccessResourcesV1Api.md#access_resources_v1_update_access_resource) | **PUT** /api/v1/orgs/{owner}/access_resources/{access_resource.uuid} | Update access resource


# **access_resources_v1_create_access_resource**
> V1AccessResource access_resources_v1_create_access_resource(owner, body)

Create access resource

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
api_instance = polyaxon_sdk.AccessResourcesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1AccessResource() # V1AccessResource | Artifact store body

try:
    # Create access resource
    api_response = api_instance.access_resources_v1_create_access_resource(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessResourcesV1Api->access_resources_v1_create_access_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body | 

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_resources_v1_delete_access_resource**
> access_resources_v1_delete_access_resource(owner, uuid)

Delete access resource

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
api_instance = polyaxon_sdk.AccessResourcesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Delete access resource
    api_instance.access_resources_v1_delete_access_resource(owner, uuid)
except ApiException as e:
    print("Exception when calling AccessResourcesV1Api->access_resources_v1_delete_access_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_resources_v1_get_access_resource**
> V1AccessResource access_resources_v1_get_access_resource(owner, uuid)

Get access resource

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
api_instance = polyaxon_sdk.AccessResourcesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get access resource
    api_response = api_instance.access_resources_v1_get_access_resource(owner, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessResourcesV1Api->access_resources_v1_get_access_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_resources_v1_list_access_resource_names**
> V1ListAccessResourcesResponse access_resources_v1_list_access_resource_names(owner, offset=offset, limit=limit, sort=sort, query=query)

List access resource names

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
api_instance = polyaxon_sdk.AccessResourcesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List access resource names
    api_response = api_instance.access_resources_v1_list_access_resource_names(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessResourcesV1Api->access_resources_v1_list_access_resource_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListAccessResourcesResponse**](V1ListAccessResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_resources_v1_list_access_resources**
> V1ListAccessResourcesResponse access_resources_v1_list_access_resources(owner, offset=offset, limit=limit, sort=sort, query=query)

List access resources

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
api_instance = polyaxon_sdk.AccessResourcesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List access resources
    api_response = api_instance.access_resources_v1_list_access_resources(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessResourcesV1Api->access_resources_v1_list_access_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListAccessResourcesResponse**](V1ListAccessResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_resources_v1_patch_access_resource**
> V1AccessResource access_resources_v1_patch_access_resource(owner, access_resource_uuid, body)

Patch access resource

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
api_instance = polyaxon_sdk.AccessResourcesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
access_resource_uuid = 'access_resource_uuid_example' # str | UUID
body = polyaxon_sdk.V1AccessResource() # V1AccessResource | Artifact store body

try:
    # Patch access resource
    api_response = api_instance.access_resources_v1_patch_access_resource(owner, access_resource_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessResourcesV1Api->access_resources_v1_patch_access_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **access_resource_uuid** | **str**| UUID | 
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body | 

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **access_resources_v1_update_access_resource**
> V1AccessResource access_resources_v1_update_access_resource(owner, access_resource_uuid, body)

Update access resource

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
api_instance = polyaxon_sdk.AccessResourcesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
access_resource_uuid = 'access_resource_uuid_example' # str | UUID
body = polyaxon_sdk.V1AccessResource() # V1AccessResource | Artifact store body

try:
    # Update access resource
    api_response = api_instance.access_resources_v1_update_access_resource(owner, access_resource_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccessResourcesV1Api->access_resources_v1_update_access_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **access_resource_uuid** | **str**| UUID | 
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body | 

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

