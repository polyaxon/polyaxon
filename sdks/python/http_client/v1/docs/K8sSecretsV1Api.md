# polyaxon_sdk.K8sSecretsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_k8s_secret**](K8sSecretsV1Api.md#create_k8s_secret) | **POST** /api/v1/orgs/{owner}/k8s_secrets | List runs
[**delete_k8s_secret**](K8sSecretsV1Api.md#delete_k8s_secret) | **DELETE** /api/v1/orgs/{owner}/k8s_secrets/{uuid} | Patch run
[**get_k8s_secret**](K8sSecretsV1Api.md#get_k8s_secret) | **GET** /api/v1/orgs/{owner}/k8s_secrets/{uuid} | Create new run
[**list_k8s_secret_names**](K8sSecretsV1Api.md#list_k8s_secret_names) | **GET** /api/v1/orgs/{owner}/k8s_secrets/names | List bookmarked runs for user
[**list_k8s_secrets**](K8sSecretsV1Api.md#list_k8s_secrets) | **GET** /api/v1/orgs/{owner}/k8s_secrets | List archived runs for user
[**patch_k8s_secret**](K8sSecretsV1Api.md#patch_k8s_secret) | **PATCH** /api/v1/orgs/{owner}/k8s_secrets/{k8s_resource.uuid} | Update run
[**update_k8s_secret**](K8sSecretsV1Api.md#update_k8s_secret) | **PUT** /api/v1/orgs/{owner}/k8s_secrets/{k8s_resource.uuid} | Get run


# **create_k8s_secret**
> V1K8sResource create_k8s_secret(owner, body)

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
api_instance = polyaxon_sdk.K8sSecretsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1K8sResource() # V1K8sResource | Artifact store body

try:
    # List runs
    api_response = api_instance.create_k8s_secret(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sSecretsV1Api->create_k8s_secret: %s\n" % e)
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

# **delete_k8s_secret**
> delete_k8s_secret(owner, uuid)

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
api_instance = polyaxon_sdk.K8sSecretsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Patch run
    api_instance.delete_k8s_secret(owner, uuid)
except ApiException as e:
    print("Exception when calling K8sSecretsV1Api->delete_k8s_secret: %s\n" % e)
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

# **get_k8s_secret**
> V1K8sResource get_k8s_secret(owner, uuid)

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
api_instance = polyaxon_sdk.K8sSecretsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Create new run
    api_response = api_instance.get_k8s_secret(owner, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sSecretsV1Api->get_k8s_secret: %s\n" % e)
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

# **list_k8s_secret_names**
> V1ListK8sResourcesResponse list_k8s_secret_names(owner, offset=offset, limit=limit, sort=sort, query=query)

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
api_instance = polyaxon_sdk.K8sSecretsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List bookmarked runs for user
    api_response = api_instance.list_k8s_secret_names(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sSecretsV1Api->list_k8s_secret_names: %s\n" % e)
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

# **list_k8s_secrets**
> V1ListK8sResourcesResponse list_k8s_secrets(owner, offset=offset, limit=limit, sort=sort, query=query)

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
api_instance = polyaxon_sdk.K8sSecretsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List archived runs for user
    api_response = api_instance.list_k8s_secrets(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sSecretsV1Api->list_k8s_secrets: %s\n" % e)
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

# **patch_k8s_secret**
> V1K8sResource patch_k8s_secret(owner, k8s_resource_uuid, body)

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
api_instance = polyaxon_sdk.K8sSecretsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
k8s_resource_uuid = 'k8s_resource_uuid_example' # str | UUID
body = polyaxon_sdk.V1K8sResource() # V1K8sResource | Artifact store body

try:
    # Update run
    api_response = api_instance.patch_k8s_secret(owner, k8s_resource_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sSecretsV1Api->patch_k8s_secret: %s\n" % e)
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

# **update_k8s_secret**
> V1K8sResource update_k8s_secret(owner, k8s_resource_uuid, body)

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
api_instance = polyaxon_sdk.K8sSecretsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
k8s_resource_uuid = 'k8s_resource_uuid_example' # str | UUID
body = polyaxon_sdk.V1K8sResource() # V1K8sResource | Artifact store body

try:
    # Get run
    api_response = api_instance.update_k8s_secret(owner, k8s_resource_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling K8sSecretsV1Api->update_k8s_secret: %s\n" % e)
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

