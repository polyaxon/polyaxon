# polyaxon_sdk.HubComponentsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_hub_component**](HubComponentsV1Api.md#create_hub_component) | **POST** /api/v1/orgs/{owner}/components | Create hub model
[**delete_hub_component**](HubComponentsV1Api.md#delete_hub_component) | **DELETE** /api/v1/orgs/{owner}/components/{uuid} | Delete hub model
[**get_hub_component**](HubComponentsV1Api.md#get_hub_component) | **GET** /api/v1/orgs/{owner}/components/{uuid} | Get hub model
[**list_hub_componebt_names**](HubComponentsV1Api.md#list_hub_componebt_names) | **GET** /api/v1/orgs/{owner}/components/names | List hub model names
[**list_hub_components**](HubComponentsV1Api.md#list_hub_components) | **GET** /api/v1/orgs/{owner}/components | List hub models
[**patch_hub_component**](HubComponentsV1Api.md#patch_hub_component) | **PATCH** /api/v1/orgs/{owner}/components/{component.uuid} | Patch hub model
[**update_hub_component**](HubComponentsV1Api.md#update_hub_component) | **PUT** /api/v1/orgs/{owner}/components/{component.uuid} | Update hub model


# **create_hub_component**
> V1HubComponent create_hub_component(owner, body)

Create hub model

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
api_instance = polyaxon_sdk.HubComponentsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1HubComponent() # V1HubComponent | Component body

try:
    # Create hub model
    api_response = api_instance.create_hub_component(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HubComponentsV1Api->create_hub_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body | 

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_hub_component**
> delete_hub_component(owner, uuid)

Delete hub model

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
api_instance = polyaxon_sdk.HubComponentsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Delete hub model
    api_instance.delete_hub_component(owner, uuid)
except ApiException as e:
    print("Exception when calling HubComponentsV1Api->delete_hub_component: %s\n" % e)
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

# **get_hub_component**
> V1HubComponent get_hub_component(owner, uuid)

Get hub model

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
api_instance = polyaxon_sdk.HubComponentsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get hub model
    api_response = api_instance.get_hub_component(owner, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HubComponentsV1Api->get_hub_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_hub_componebt_names**
> V1ListHubComponentsResponse list_hub_componebt_names(owner, offset=offset, limit=limit, sort=sort, query=query)

List hub model names

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
api_instance = polyaxon_sdk.HubComponentsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List hub model names
    api_response = api_instance.list_hub_componebt_names(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HubComponentsV1Api->list_hub_componebt_names: %s\n" % e)
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

[**V1ListHubComponentsResponse**](V1ListHubComponentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_hub_components**
> V1ListHubComponentsResponse list_hub_components(owner, offset=offset, limit=limit, sort=sort, query=query)

List hub models

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
api_instance = polyaxon_sdk.HubComponentsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List hub models
    api_response = api_instance.list_hub_components(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HubComponentsV1Api->list_hub_components: %s\n" % e)
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

[**V1ListHubComponentsResponse**](V1ListHubComponentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_hub_component**
> V1HubComponent patch_hub_component(owner, component_uuid, body)

Patch hub model

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
api_instance = polyaxon_sdk.HubComponentsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
component_uuid = 'component_uuid_example' # str | UUID
body = polyaxon_sdk.V1HubComponent() # V1HubComponent | Component body

try:
    # Patch hub model
    api_response = api_instance.patch_hub_component(owner, component_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HubComponentsV1Api->patch_hub_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **component_uuid** | **str**| UUID | 
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body | 

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_hub_component**
> V1HubComponent update_hub_component(owner, component_uuid, body)

Update hub model

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
api_instance = polyaxon_sdk.HubComponentsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
component_uuid = 'component_uuid_example' # str | UUID
body = polyaxon_sdk.V1HubComponent() # V1HubComponent | Component body

try:
    # Update hub model
    api_response = api_instance.update_hub_component(owner, component_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HubComponentsV1Api->update_hub_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **component_uuid** | **str**| UUID | 
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body | 

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

