# polyaxon_sdk.K8sConfigMapsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_k8s_config_map**](K8sConfigMapsV1Api.md#create_k8s_config_map) | **POST** /api/v1/orgs/{owner}/k8s_config_maps | List runs
[**delete_k8s_config_map**](K8sConfigMapsV1Api.md#delete_k8s_config_map) | **DELETE** /api/v1/orgs/{owner}/k8s_config_maps/{uuid} | Patch run
[**get_k8s_config_map**](K8sConfigMapsV1Api.md#get_k8s_config_map) | **GET** /api/v1/orgs/{owner}/k8s_config_maps/{uuid} | Create new run
[**list_k8s_config_map_names**](K8sConfigMapsV1Api.md#list_k8s_config_map_names) | **GET** /api/v1/orgs/{owner}/k8s_config_maps/names | List bookmarked runs for user
[**list_k8s_config_maps**](K8sConfigMapsV1Api.md#list_k8s_config_maps) | **GET** /api/v1/orgs/{owner}/k8s_config_maps | List archived runs for user
[**patch_k8s_config_map**](K8sConfigMapsV1Api.md#patch_k8s_config_map) | **PATCH** /api/v1/orgs/{owner}/k8s_config_maps/{k8s_resource.uuid} | Update run
[**update_k8s_config_map**](K8sConfigMapsV1Api.md#update_k8s_config_map) | **PUT** /api/v1/orgs/{owner}/k8s_config_maps/{k8s_resource.uuid} | Get run


# **create_k8s_config_map**
> V1K8sResource create_k8s_config_map(owner, body)

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
api_instance = polyaxon_sdk.K8sConfigMapsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1K8sResource() # V1K8sResource | Artifact store body

try:
    # List runs
    api_response = api_instance.create_k8s_config_map(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sConfigMapsV1Api->create_k8s_config_map: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body | 

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_k8s_config_map**
> delete_k8s_config_map(owner, uuid)

Patch run

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
api_instance = polyaxon_sdk.K8sConfigMapsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Patch run
    api_instance.delete_k8s_config_map(owner, uuid)
except ApiException as e:
    print("Exception when calling K8sConfigMapsV1Api->delete_k8s_config_map: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_k8s_config_map**
> V1K8sResource get_k8s_config_map(owner, uuid)

Create new run

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
api_instance = polyaxon_sdk.K8sConfigMapsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Create new run
    api_response = api_instance.get_k8s_config_map(owner, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sConfigMapsV1Api->get_k8s_config_map: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_k8s_config_map_names**
> V1ListK8sResourcesResponse list_k8s_config_map_names(owner, offset=offset, limit=limit, sort=sort, query=query)

List bookmarked runs for user

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
api_instance = polyaxon_sdk.K8sConfigMapsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List bookmarked runs for user
    api_response = api_instance.list_k8s_config_map_names(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sConfigMapsV1Api->list_k8s_config_map_names: %s\n" % e)
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

[**V1ListK8sResourcesResponse**](V1ListK8sResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_k8s_config_maps**
> V1ListK8sResourcesResponse list_k8s_config_maps(owner, offset=offset, limit=limit, sort=sort, query=query)

List archived runs for user

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
api_instance = polyaxon_sdk.K8sConfigMapsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List archived runs for user
    api_response = api_instance.list_k8s_config_maps(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sConfigMapsV1Api->list_k8s_config_maps: %s\n" % e)
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

[**V1ListK8sResourcesResponse**](V1ListK8sResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_k8s_config_map**
> V1K8sResource patch_k8s_config_map(owner, k8s_resource_uuid, body)

Update run

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
api_instance = polyaxon_sdk.K8sConfigMapsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
k8s_resource_uuid = 'k8s_resource_uuid_example' # str | UUID
body = polyaxon_sdk.V1K8sResource() # V1K8sResource | Artifact store body

try:
    # Update run
    api_response = api_instance.patch_k8s_config_map(owner, k8s_resource_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sConfigMapsV1Api->patch_k8s_config_map: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **k8s_resource_uuid** | **str**| UUID | 
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body | 

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_k8s_config_map**
> V1K8sResource update_k8s_config_map(owner, k8s_resource_uuid, body)

Get run

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
api_instance = polyaxon_sdk.K8sConfigMapsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
k8s_resource_uuid = 'k8s_resource_uuid_example' # str | UUID
body = polyaxon_sdk.V1K8sResource() # V1K8sResource | Artifact store body

try:
    # Get run
    api_response = api_instance.update_k8s_config_map(owner, k8s_resource_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sConfigMapsV1Api->update_k8s_config_map: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **k8s_resource_uuid** | **str**| UUID | 
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body | 

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

