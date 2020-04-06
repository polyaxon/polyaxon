# polyaxon_sdk.ConnectionsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**connections_v1_create_connection**](ConnectionsV1Api.md#connections_v1_create_connection) | **POST** /api/v1/orgs/{owner}/connections | Create connection
[**connections_v1_delete_connection**](ConnectionsV1Api.md#connections_v1_delete_connection) | **DELETE** /api/v1/orgs/{owner}/connections/{uuid} | Delete connection
[**connections_v1_get_connection**](ConnectionsV1Api.md#connections_v1_get_connection) | **GET** /api/v1/orgs/{owner}/connections/{uuid} | Get connection
[**connections_v1_list_connection_names**](ConnectionsV1Api.md#connections_v1_list_connection_names) | **GET** /api/v1/orgs/{owner}/connections/names | List connections names
[**connections_v1_list_connections**](ConnectionsV1Api.md#connections_v1_list_connections) | **GET** /api/v1/orgs/{owner}/connections | List connections
[**connections_v1_patch_connection**](ConnectionsV1Api.md#connections_v1_patch_connection) | **PATCH** /api/v1/orgs/{owner}/connections/{connection.uuid} | Patch connection
[**connections_v1_update_connection**](ConnectionsV1Api.md#connections_v1_update_connection) | **PUT** /api/v1/orgs/{owner}/connections/{connection.uuid} | Update connection


# **connections_v1_create_connection**
> V1ConnectionResponse connections_v1_create_connection(owner, body)

Create connection

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
api_instance = polyaxon_sdk.ConnectionsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1ConnectionResponse() # V1ConnectionResponse | Connection body

try:
    # Create connection
    api_response = api_instance.connections_v1_create_connection(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsV1Api->connections_v1_create_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body | 

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **connections_v1_delete_connection**
> connections_v1_delete_connection(owner, uuid)

Delete connection

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
api_instance = polyaxon_sdk.ConnectionsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Delete connection
    api_instance.connections_v1_delete_connection(owner, uuid)
except ApiException as e:
    print("Exception when calling ConnectionsV1Api->connections_v1_delete_connection: %s\n" % e)
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

# **connections_v1_get_connection**
> V1ConnectionResponse connections_v1_get_connection(owner, uuid)

Get connection

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
api_instance = polyaxon_sdk.ConnectionsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get connection
    api_response = api_instance.connections_v1_get_connection(owner, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsV1Api->connections_v1_get_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **connections_v1_list_connection_names**
> V1ListConnectionsResponse connections_v1_list_connection_names(owner, offset=offset, limit=limit, sort=sort, query=query)

List connections names

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
api_instance = polyaxon_sdk.ConnectionsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List connections names
    api_response = api_instance.connections_v1_list_connection_names(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsV1Api->connections_v1_list_connection_names: %s\n" % e)
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

[**V1ListConnectionsResponse**](V1ListConnectionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **connections_v1_list_connections**
> V1ListConnectionsResponse connections_v1_list_connections(owner, offset=offset, limit=limit, sort=sort, query=query)

List connections

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
api_instance = polyaxon_sdk.ConnectionsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List connections
    api_response = api_instance.connections_v1_list_connections(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsV1Api->connections_v1_list_connections: %s\n" % e)
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

[**V1ListConnectionsResponse**](V1ListConnectionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **connections_v1_patch_connection**
> V1ConnectionResponse connections_v1_patch_connection(owner, connection_uuid, body)

Patch connection

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
api_instance = polyaxon_sdk.ConnectionsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
connection_uuid = 'connection_uuid_example' # str | UUID
body = polyaxon_sdk.V1ConnectionResponse() # V1ConnectionResponse | Connection body

try:
    # Patch connection
    api_response = api_instance.connections_v1_patch_connection(owner, connection_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsV1Api->connections_v1_patch_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **connection_uuid** | **str**| UUID | 
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body | 

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **connections_v1_update_connection**
> V1ConnectionResponse connections_v1_update_connection(owner, connection_uuid, body)

Update connection

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
api_instance = polyaxon_sdk.ConnectionsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
connection_uuid = 'connection_uuid_example' # str | UUID
body = polyaxon_sdk.V1ConnectionResponse() # V1ConnectionResponse | Connection body

try:
    # Update connection
    api_response = api_instance.connections_v1_update_connection(owner, connection_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionsV1Api->connections_v1_update_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **connection_uuid** | **str**| UUID | 
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body | 

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

