# polyaxon_sdk.RunsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_run**](RunsV1Api.md#archive_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/archive | Archive run
[**bookmark_run**](RunsV1Api.md#bookmark_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/bookmark | Bookmark run
[**copy_run**](RunsV1Api.md#copy_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/copy | Restart run with copy
[**create_run**](RunsV1Api.md#create_run) | **POST** /api/v1/{owner}/{project}/runs | Create new run
[**create_run_code_ref**](RunsV1Api.md#create_run_code_ref) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/coderef | Get run code ref
[**create_run_status**](RunsV1Api.md#create_run_status) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Create new run status
[**delete_run**](RunsV1Api.md#delete_run) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid} | Delete run
[**delete_runs**](RunsV1Api.md#delete_runs) | **DELETE** /api/v1/{owner}/{project}/runs/delete | Delete runs
[**get_run**](RunsV1Api.md#get_run) | **GET** /api/v1/{owner}/{project}/runs/{uuid} | Get run
[**get_run_code_refs**](RunsV1Api.md#get_run_code_refs) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/coderef | Get run code ref
[**get_run_statuses**](RunsV1Api.md#get_run_statuses) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Get run status
[**invalidate_run**](RunsV1Api.md#invalidate_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/invalidate | Stop run
[**invalidate_runs**](RunsV1Api.md#invalidate_runs) | **POST** /api/v1/{owner}/{project}/runs/invalidate | Invalidate runs
[**list_archived_runs**](RunsV1Api.md#list_archived_runs) | **GET** /api/v1/archives/{user}/runs | List archived runs for user
[**list_bookmarked_runs**](RunsV1Api.md#list_bookmarked_runs) | **GET** /api/v1/bookmarks/{user}/runs | List bookmarked runs for user
[**list_runs**](RunsV1Api.md#list_runs) | **GET** /api/v1/{owner}/{project}/runs | List runs
[**patch_run**](RunsV1Api.md#patch_run) | **PATCH** /api/v1/{owner}/{project}/runs/{run.uuid} | Patch run
[**restart_run**](RunsV1Api.md#restart_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/restart | Restart run
[**restore_run**](RunsV1Api.md#restore_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/restore | Restore run
[**resume_run**](RunsV1Api.md#resume_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/resume | Resume run
[**start_run_tensorboard**](RunsV1Api.md#start_run_tensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/start | Start run tensorboard
[**stop_run**](RunsV1Api.md#stop_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/stop | Stop run
[**stop_run_tensorboard**](RunsV1Api.md#stop_run_tensorboard) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/stop | Stop run tensorboard
[**stop_runs**](RunsV1Api.md#stop_runs) | **POST** /api/v1/{owner}/{project}/runs/stop | Stop runs
[**unbookmark_run**](RunsV1Api.md#unbookmark_run) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/unbookmark | Unbookmark run
[**update_run**](RunsV1Api.md#update_run) | **PUT** /api/v1/{owner}/{project}/runs/{run.uuid} | Update run


# **archive_run**
> object archive_run(owner, project, uuid)

Archive run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Archive run
    api_response = api_instance.archive_run(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->archive_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bookmark_run**
> object bookmark_run(owner, project, uuid)

Bookmark run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Bookmark run
    api_response = api_instance.bookmark_run(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->bookmark_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **copy_run**
> V1Run copy_run(owner, project, uuid, body)

Restart run with copy

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityUUIdRequest() # V1OwnedEntityUUIdRequest | 

try:
    # Restart run with copy
    api_response = api_instance.copy_run(owner, project, uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->copy_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityUUIdRequest**](V1OwnedEntityUUIdRequest.md)|  | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_run**
> V1Run create_run(owner, project, body)

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = polyaxon_sdk.V1RunBodyRequest() # V1RunBodyRequest | 

try:
    # Create new run
    api_response = api_instance.create_run(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->create_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **body** | [**V1RunBodyRequest**](V1RunBodyRequest.md)|  | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_run_code_ref**
> V1CodeReference create_run_code_ref(entity_owner, entity_project, entity_uuid, body)

Get run code ref

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project where the experiement will be assigned
entity_uuid = 'entity_uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1CodeRefBodyRequest() # V1CodeRefBodyRequest | 

try:
    # Get run code ref
    api_response = api_instance.create_run_code_ref(entity_owner, entity_project, entity_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->create_run_code_ref: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project where the experiement will be assigned | 
 **entity_uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1CodeRefBodyRequest**](V1CodeRefBodyRequest.md)|  | 

### Return type

[**V1CodeReference**](V1CodeReference.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_run_status**
> V1Status create_run_status(owner, project, uuid, body)

Create new run status

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1EntityStatusRequest() # V1EntityStatusRequest | 

try:
    # Create new run status
    api_response = api_instance.create_run_status(owner, project, uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->create_run_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1EntityStatusRequest**](V1EntityStatusRequest.md)|  | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_run**
> object delete_run(owner, project, uuid)

Delete run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Delete run
    api_response = api_instance.delete_run(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->delete_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_runs**
> object delete_runs(owner, project, body)

Delete runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Delete runs
    api_response = api_instance.delete_runs(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->delete_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run**
> V1Run get_run(owner, project, uuid)

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Get run
    api_response = api_instance.get_run(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run_code_refs**
> V1ListCodeRefResponse get_run_code_refs(owner, project, uuid)

Get run code ref

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Get run code ref
    api_response = api_instance.get_run_code_refs(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run_code_refs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1ListCodeRefResponse**](V1ListCodeRefResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run_statuses**
> V1Status get_run_statuses(owner, project, uuid)

Get run status

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Get run status
    api_response = api_instance.get_run_statuses(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run_statuses: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **invalidate_run**
> object invalidate_run(owner, project, uuid, body)

Stop run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityUUIdRequest() # V1OwnedEntityUUIdRequest | 

try:
    # Stop run
    api_response = api_instance.invalidate_run(owner, project, uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->invalidate_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityUUIdRequest**](V1OwnedEntityUUIdRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **invalidate_runs**
> object invalidate_runs(owner, project, body)

Invalidate runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Invalidate runs
    api_response = api_instance.invalidate_runs(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->invalidate_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_archived_runs**
> V1ListRunsResponse list_archived_runs(user)

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
user = 'user_example' # str | Owner of the namespace

try:
    # List archived runs for user
    api_response = api_instance.list_archived_runs(user)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->list_archived_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| Owner of the namespace | 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_bookmarked_runs**
> V1ListRunsResponse list_bookmarked_runs(user)

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
user = 'user_example' # str | Owner of the namespace

try:
    # List bookmarked runs for user
    api_response = api_instance.list_bookmarked_runs(user)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->list_bookmarked_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| Owner of the namespace | 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_runs**
> V1ListRunsResponse list_runs(owner, project)

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # List runs
    api_response = api_instance.list_runs(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->list_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_run**
> V1Run patch_run(owner, project, run_uuid, body)

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
run_uuid = 'run_uuid_example' # str | UUID
body = polyaxon_sdk.V1RunBodyRequest() # V1RunBodyRequest | 

try:
    # Patch run
    api_response = api_instance.patch_run(owner, project, run_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->patch_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **run_uuid** | **str**| UUID | 
 **body** | [**V1RunBodyRequest**](V1RunBodyRequest.md)|  | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restart_run**
> V1Run restart_run(owner, project, uuid, body)

Restart run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityUUIdRequest() # V1OwnedEntityUUIdRequest | 

try:
    # Restart run
    api_response = api_instance.restart_run(owner, project, uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->restart_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityUUIdRequest**](V1OwnedEntityUUIdRequest.md)|  | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_run**
> object restore_run(owner, project, uuid)

Restore run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Restore run
    api_response = api_instance.restore_run(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->restore_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_run**
> V1Run resume_run(owner, project, uuid, body)

Resume run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityUUIdRequest() # V1OwnedEntityUUIdRequest | 

try:
    # Resume run
    api_response = api_instance.resume_run(owner, project, uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->resume_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityUUIdRequest**](V1OwnedEntityUUIdRequest.md)|  | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_run_tensorboard**
> object start_run_tensorboard(owner, project, uuid, body)

Start run tensorboard

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityUUIdRequest() # V1OwnedEntityUUIdRequest | 

try:
    # Start run tensorboard
    api_response = api_instance.start_run_tensorboard(owner, project, uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->start_run_tensorboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityUUIdRequest**](V1OwnedEntityUUIdRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_run**
> object stop_run(owner, project, uuid, body)

Stop run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1OwnedEntityUUIdRequest() # V1OwnedEntityUUIdRequest | 

try:
    # Stop run
    api_response = api_instance.stop_run(owner, project, uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->stop_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityUUIdRequest**](V1OwnedEntityUUIdRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_run_tensorboard**
> object stop_run_tensorboard(owner, project, uuid)

Stop run tensorboard

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Stop run tensorboard
    api_response = api_instance.stop_run_tensorboard(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->stop_run_tensorboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_runs**
> object stop_runs(owner, project, body)

Stop runs

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Stop runs
    api_response = api_instance.stop_runs(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->stop_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unbookmark_run**
> object unbookmark_run(owner, project, uuid)

Unbookmark run

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Unbookmark run
    api_response = api_instance.unbookmark_run(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->unbookmark_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_run**
> V1Run update_run(owner, project, run_uuid, body)

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
api_instance = polyaxon_sdk.RunsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
run_uuid = 'run_uuid_example' # str | UUID
body = polyaxon_sdk.V1RunBodyRequest() # V1RunBodyRequest | 

try:
    # Update run
    api_response = api_instance.update_run(owner, project, run_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->update_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **run_uuid** | **str**| UUID | 
 **body** | [**V1RunBodyRequest**](V1RunBodyRequest.md)|  | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

