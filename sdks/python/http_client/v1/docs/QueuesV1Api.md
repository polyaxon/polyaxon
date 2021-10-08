# polyaxon_sdk.QueuesV1Api
Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_queue**](QueuesV1Api.md#create_queue) | **POST** /api/v1/orgs/{owner}/agents/{agent}/queues | Create queue
[**delete_queue**](QueuesV1Api.md#delete_queue) | **DELETE** /api/v1/orgs/{owner}/agents/{entity}/queues/{uuid} | Delete queue
[**get_queue**](QueuesV1Api.md#get_queue) | **GET** /api/v1/orgs/{owner}/agents/{entity}/queues/{uuid} | Get queue
[**list_organization_queue_names**](QueuesV1Api.md#list_organization_queue_names) | **GET** /api/v1/orgs/{owner}/queues/names | List organization level queues names
[**list_organization_queues**](QueuesV1Api.md#list_organization_queues) | **GET** /api/v1/orgs/{owner}/queues | List organization level queues
[**list_queue_names**](QueuesV1Api.md#list_queue_names) | **GET** /api/v1/orgs/{owner}/agents/{name}/queues/names | List queues names
[**list_queues**](QueuesV1Api.md#list_queues) | **GET** /api/v1/orgs/{owner}/agents/{name}/queues | List queues
[**patch_queue**](QueuesV1Api.md#patch_queue) | **PATCH** /api/v1/orgs/{owner}/agents/{agent}/queues/{queue.uuid} | Patch queue
[**update_queue**](QueuesV1Api.md#update_queue) | **PUT** /api/v1/orgs/{owner}/agents/{agent}/queues/{queue.uuid} | Update queue


# **create_queue**
> V1Queue create_queue(owner, agent, body)

Create queue

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
agent = 'agent_example' # str | Agent that consumes the queue
body = polyaxon_sdk.V1Queue() # V1Queue | Queue body

    try:
        # Create queue
        api_response = api_instance.create_queue(owner, agent, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->create_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **agent** | **str**| Agent that consumes the queue | 
 **body** | [**V1Queue**](V1Queue.md)| Queue body | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_queue**
> delete_queue(owner, entity, uuid)

Delete queue

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
entity = 'entity_example' # str | Entity: project name, hub name, registry name, ...
uuid = 'uuid_example' # str | Uuid identifier of the sub-entity

    try:
        # Delete queue
        api_instance.delete_queue(owner, entity, uuid)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->delete_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **entity** | **str**| Entity: project name, hub name, registry name, ... | 
 **uuid** | **str**| Uuid identifier of the sub-entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_queue**
> V1Queue get_queue(owner, entity, uuid)

Get queue

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
entity = 'entity_example' # str | Entity: project name, hub name, registry name, ...
uuid = 'uuid_example' # str | Uuid identifier of the sub-entity

    try:
        # Get queue
        api_response = api_instance.get_queue(owner, entity, uuid)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->get_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **entity** | **str**| Entity: project name, hub name, registry name, ... | 
 **uuid** | **str**| Uuid identifier of the sub-entity | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_organization_queue_names**
> V1ListQueuesResponse list_organization_queue_names(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)

List organization level queues names

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search. (optional)
bookmarks = True # bool | Filter by bookmarks. (optional)
pins = 'pins_example' # str | Pinned entities. (optional)
mode = 'mode_example' # str | Mode of the search. (optional)
no_page = True # bool | No pagination. (optional)

    try:
        # List organization level queues names
        api_response = api_instance.list_organization_queue_names(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->list_organization_queue_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search. | [optional] 
 **bookmarks** | **bool**| Filter by bookmarks. | [optional] 
 **pins** | **str**| Pinned entities. | [optional] 
 **mode** | **str**| Mode of the search. | [optional] 
 **no_page** | **bool**| No pagination. | [optional] 

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_organization_queues**
> V1ListQueuesResponse list_organization_queues(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)

List organization level queues

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search. (optional)
bookmarks = True # bool | Filter by bookmarks. (optional)
pins = 'pins_example' # str | Pinned entities. (optional)
mode = 'mode_example' # str | Mode of the search. (optional)
no_page = True # bool | No pagination. (optional)

    try:
        # List organization level queues
        api_response = api_instance.list_organization_queues(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->list_organization_queues: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search. | [optional] 
 **bookmarks** | **bool**| Filter by bookmarks. | [optional] 
 **pins** | **str**| Pinned entities. | [optional] 
 **mode** | **str**| Mode of the search. | [optional] 
 **no_page** | **bool**| No pagination. | [optional] 

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_queue_names**
> V1ListQueuesResponse list_queue_names(owner, name, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)

List queues names

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
name = 'name_example' # str | Entity managing the resource
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search. (optional)
bookmarks = True # bool | Filter by bookmarks. (optional)
pins = 'pins_example' # str | Pinned entities. (optional)
mode = 'mode_example' # str | Mode of the search. (optional)
no_page = True # bool | No pagination. (optional)

    try:
        # List queues names
        api_response = api_instance.list_queue_names(owner, name, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->list_queue_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **name** | **str**| Entity managing the resource | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search. | [optional] 
 **bookmarks** | **bool**| Filter by bookmarks. | [optional] 
 **pins** | **str**| Pinned entities. | [optional] 
 **mode** | **str**| Mode of the search. | [optional] 
 **no_page** | **bool**| No pagination. | [optional] 

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_queues**
> V1ListQueuesResponse list_queues(owner, name, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)

List queues

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
name = 'name_example' # str | Entity managing the resource
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search. (optional)
bookmarks = True # bool | Filter by bookmarks. (optional)
pins = 'pins_example' # str | Pinned entities. (optional)
mode = 'mode_example' # str | Mode of the search. (optional)
no_page = True # bool | No pagination. (optional)

    try:
        # List queues
        api_response = api_instance.list_queues(owner, name, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->list_queues: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **name** | **str**| Entity managing the resource | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search. | [optional] 
 **bookmarks** | **bool**| Filter by bookmarks. | [optional] 
 **pins** | **str**| Pinned entities. | [optional] 
 **mode** | **str**| Mode of the search. | [optional] 
 **no_page** | **bool**| No pagination. | [optional] 

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_queue**
> V1Queue patch_queue(owner, agent, queue_uuid, body)

Patch queue

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
agent = 'agent_example' # str | Agent that consumes the queue
queue_uuid = 'queue_uuid_example' # str | UUID
body = polyaxon_sdk.V1Queue() # V1Queue | Queue body

    try:
        # Patch queue
        api_response = api_instance.patch_queue(owner, agent, queue_uuid, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->patch_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **agent** | **str**| Agent that consumes the queue | 
 **queue_uuid** | **str**| UUID | 
 **body** | [**V1Queue**](V1Queue.md)| Queue body | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_queue**
> V1Queue update_queue(owner, agent, queue_uuid, body)

Update queue

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
    api_instance = polyaxon_sdk.QueuesV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
agent = 'agent_example' # str | Agent that consumes the queue
queue_uuid = 'queue_uuid_example' # str | UUID
body = polyaxon_sdk.V1Queue() # V1Queue | Queue body

    try:
        # Update queue
        api_response = api_instance.update_queue(owner, agent, queue_uuid, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling QueuesV1Api->update_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **agent** | **str**| Agent that consumes the queue | 
 **queue_uuid** | **str**| UUID | 
 **body** | [**V1Queue**](V1Queue.md)| Queue body | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

