# polyaxon_sdk.QueuesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**queues_v1_create_queue**](QueuesV1Api.md#queues_v1_create_queue) | **POST** /api/v1/orgs/{owner}/agents/{agent}/queues | Update agent
[**queues_v1_delete_queue**](QueuesV1Api.md#queues_v1_delete_queue) | **DELETE** /api/v1/orgs/{owner}/agents/{agent}/queues/{uuid} | Sync agent
[**queues_v1_get_queue**](QueuesV1Api.md#queues_v1_get_queue) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues/{uuid} | Patch agent
[**queues_v1_list_organization_queue_names**](QueuesV1Api.md#queues_v1_list_organization_queue_names) | **GET** /api/v1/orgs/{owner}/queues/names | List agents names
[**queues_v1_list_organization_queues**](QueuesV1Api.md#queues_v1_list_organization_queues) | **GET** /api/v1/orgs/{owner}/queues | List agents
[**queues_v1_list_queue_names**](QueuesV1Api.md#queues_v1_list_queue_names) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues/names | Create agent
[**queues_v1_list_queues**](QueuesV1Api.md#queues_v1_list_queues) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues | Get agent
[**queues_v1_patch_queue**](QueuesV1Api.md#queues_v1_patch_queue) | **PATCH** /api/v1/orgs/{owner}/agents/{queue.agent}/queues/{queue.uuid} | Get State (queues/runs)
[**queues_v1_update_queue**](QueuesV1Api.md#queues_v1_update_queue) | **PUT** /api/v1/orgs/{owner}/agents/{queue.agent}/queues/{queue.uuid} | Delete agent


# **queues_v1_create_queue**
> V1Agent queues_v1_create_queue(owner, agent, body)

Update agent

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
agent = 'agent_example' # str | Agent that consumes the queue
body = polyaxon_sdk.V1Queue() # V1Queue | Queue body

try:
    # Update agent
    api_response = api_instance.queues_v1_create_queue(owner, agent, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_create_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **agent** | **str**| Agent that consumes the queue | 
 **body** | [**V1Queue**](V1Queue.md)| Queue body | 

### Return type

[**V1Agent**](V1Agent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queues_v1_delete_queue**
> queues_v1_delete_queue(owner, agent, uuid)

Sync agent

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
agent = 'agent_example' # str | Agent managing the resource
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Sync agent
    api_instance.queues_v1_delete_queue(owner, agent, uuid)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_delete_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **agent** | **str**| Agent managing the resource | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queues_v1_get_queue**
> V1Queue queues_v1_get_queue(owner, agent, uuid)

Patch agent

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
agent = 'agent_example' # str | Agent managing the resource
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Patch agent
    api_response = api_instance.queues_v1_get_queue(owner, agent, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_get_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **agent** | **str**| Agent managing the resource | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queues_v1_list_organization_queue_names**
> V1ListQueuesResponse queues_v1_list_organization_queue_names(owner, offset=offset, limit=limit, sort=sort, query=query)

List agents names

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List agents names
    api_response = api_instance.queues_v1_list_organization_queue_names(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_list_organization_queue_names: %s\n" % e)
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

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queues_v1_list_organization_queues**
> V1ListQueuesResponse queues_v1_list_organization_queues(owner, offset=offset, limit=limit, sort=sort, query=query)

List agents

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List agents
    api_response = api_instance.queues_v1_list_organization_queues(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_list_organization_queues: %s\n" % e)
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

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queues_v1_list_queue_names**
> V1ListQueuesResponse queues_v1_list_queue_names(owner, agent, offset=offset, limit=limit, sort=sort, query=query)

Create agent

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
agent = 'agent_example' # str | Agent man managing the resource
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # Create agent
    api_response = api_instance.queues_v1_list_queue_names(owner, agent, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_list_queue_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **agent** | **str**| Agent man managing the resource | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queues_v1_list_queues**
> V1ListQueuesResponse queues_v1_list_queues(owner, agent, offset=offset, limit=limit, sort=sort, query=query)

Get agent

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
agent = 'agent_example' # str | Agent man managing the resource
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # Get agent
    api_response = api_instance.queues_v1_list_queues(owner, agent, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_list_queues: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **agent** | **str**| Agent man managing the resource | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queues_v1_patch_queue**
> V1Queue queues_v1_patch_queue(owner, queue_agent, queue_uuid, body)

Get State (queues/runs)

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
queue_agent = 'queue_agent_example' # str | Agent
queue_uuid = 'queue_uuid_example' # str | UUID
body = polyaxon_sdk.V1Queue() # V1Queue | Queue body

try:
    # Get State (queues/runs)
    api_response = api_instance.queues_v1_patch_queue(owner, queue_agent, queue_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_patch_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **queue_agent** | **str**| Agent | 
 **queue_uuid** | **str**| UUID | 
 **body** | [**V1Queue**](V1Queue.md)| Queue body | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queues_v1_update_queue**
> V1Queue queues_v1_update_queue(owner, queue_agent, queue_uuid, body)

Delete agent

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
api_instance = polyaxon_sdk.QueuesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
queue_agent = 'queue_agent_example' # str | Agent
queue_uuid = 'queue_uuid_example' # str | UUID
body = polyaxon_sdk.V1Queue() # V1Queue | Queue body

try:
    # Delete agent
    api_response = api_instance.queues_v1_update_queue(owner, queue_agent, queue_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueuesV1Api->queues_v1_update_queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **queue_agent** | **str**| Agent | 
 **queue_uuid** | **str**| UUID | 
 **body** | [**V1Queue**](V1Queue.md)| Queue body | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

