# polyaxon_sdk.RunsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_run**](RunsV1Api.md#archive_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/archive | Archive run
[**bookmark_run**](RunsV1Api.md#bookmark_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/bookmark | Bookmark run
[**copy_run**](RunsV1Api.md#copy_run) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/copy | Restart run with copy
[**create_run**](RunsV1Api.md#create_run) | **POST** /api/v1/{owner}/{project}/runs | Create new run
[**create_run_code_ref**](RunsV1Api.md#create_run_code_ref) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/coderefs | Get run code ref
[**create_run_status**](RunsV1Api.md#create_run_status) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Create new run status
[**delete_run**](RunsV1Api.md#delete_run) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid} | Delete run
[**delete_runs**](RunsV1Api.md#delete_runs) | **DELETE** /api/v1/{owner}/{project}/runs/delete | Delete runs
[**get_run**](RunsV1Api.md#get_run) | **GET** /api/v1/{owner}/{project}/runs/{uuid} | Get run
[**get_run_artifacts_tree**](RunsV1Api.md#get_run_artifacts_tree) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts/tree | Get run artifacts list
[**get_run_logs_file**](RunsV1Api.md#get_run_logs_file) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/logs/file | Get run logs get file
[**get_run_logs_tree**](RunsV1Api.md#get_run_logs_tree) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/logs/tree | Get run logs list
[**get_run_settings**](RunsV1Api.md#get_run_settings) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/settings | Get Run settings
[**get_run_statuses**](RunsV1Api.md#get_run_statuses) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Get run status
[**impersonate_token**](RunsV1Api.md#impersonate_token) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/impersonate | Impersonate run token
[**invalidate_run**](RunsV1Api.md#invalidate_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/invalidate | Invalidate run
[**invalidate_runs**](RunsV1Api.md#invalidate_runs) | **POST** /api/v1/{owner}/{project}/runs/invalidate | Invalidate runs
[**list_archived_runs**](RunsV1Api.md#list_archived_runs) | **GET** /api/v1/archives/{user}/runs | List archived runs for user
[**list_bookmarked_runs**](RunsV1Api.md#list_bookmarked_runs) | **GET** /api/v1/bookmarks/{user}/runs | List bookmarked runs for user
[**list_runs**](RunsV1Api.md#list_runs) | **GET** /api/v1/{owner}/{project}/runs | List runs
[**patch_run**](RunsV1Api.md#patch_run) | **PATCH** /api/v1/{owner}/{project}/runs/{run.uuid} | Patch run
[**restart_run**](RunsV1Api.md#restart_run) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/restart | Restart run
[**restore_run**](RunsV1Api.md#restore_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/restore | Restore run
[**resume_run**](RunsV1Api.md#resume_run) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/resume | Resume run
[**start_run_tensorboard**](RunsV1Api.md#start_run_tensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/start | Start run tensorboard
[**stop_run**](RunsV1Api.md#stop_run) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/stop | Stop run
[**stop_run_tensorboard**](RunsV1Api.md#stop_run_tensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/stop | Stop run tensorboard
[**stop_runs**](RunsV1Api.md#stop_runs) | **POST** /api/v1/{owner}/{project}/runs/stop | Stop runs
[**unbookmark_run**](RunsV1Api.md#unbookmark_run) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/unbookmark | Unbookmark run
[**update_run**](RunsV1Api.md#update_run) | **PUT** /api/v1/{owner}/{project}/runs/{run.uuid} | Update run
[**upload_run_artifact**](RunsV1Api.md#upload_run_artifact) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/artifacts/upload | Upload an artifact file to a store via run access
[**upload_run_logs**](RunsV1Api.md#upload_run_logs) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/logs/upload | Upload a logs file to a store via run access


# **archive_run**
> archive_run(owner, project, uuid)

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
    api_instance.archive_run(owner, project, uuid)
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

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bookmark_run**
> bookmark_run(owner, project, uuid)

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
    api_instance.bookmark_run(owner, project, uuid)
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

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **copy_run**
> V1Run copy_run(entity_owner, entity_project, entity_uuid, body)

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
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project where the experiement will be assigned
entity_uuid = 'entity_uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1Run() # V1Run | Run object

try:
    # Restart run with copy
    api_response = api_instance.copy_run(entity_owner, entity_project, entity_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->copy_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project where the experiement will be assigned | 
 **entity_uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

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
body = polyaxon_sdk.V1Run() # V1Run | Run object

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
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_run_code_ref**
> create_run_code_ref(entity_owner, entity_project, entity_uuid, body)

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
body = polyaxon_sdk.V1CodeRef() # V1CodeRef | Code ref object

try:
    # Get run code ref
    api_instance.create_run_code_ref(entity_owner, entity_project, entity_uuid, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->create_run_code_ref: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project where the experiement will be assigned | 
 **entity_uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1CodeRef**](V1CodeRef.md)| Code ref object | 

### Return type

void (empty response body)

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
body = polyaxon_sdk.V1EntityStatusBodyRequest() # V1EntityStatusBodyRequest | 

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
 **body** | [**V1EntityStatusBodyRequest**](V1EntityStatusBodyRequest.md)|  | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_run**
> delete_run(owner, project, uuid)

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
    api_instance.delete_run(owner, project, uuid)
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

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_runs**
> delete_runs(owner, project, body)

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
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

try:
    # Delete runs
    api_instance.delete_runs(owner, project, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->delete_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

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

# **get_run_artifacts_tree**
> V1ArtifactTreeResponse get_run_artifacts_tree(owner, project, uuid, path=path, step=step, kind=kind)

Get run artifacts list

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
path = 'path_example' # str | Artifact filepath. (optional)
step = 56 # int | Artifact logging step. (optional)
kind = 'kind_example' # str | Artifact kind. (optional)

try:
    # Get run artifacts list
    api_response = api_instance.get_run_artifacts_tree(owner, project, uuid, path=path, step=step, kind=kind)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run_artifacts_tree: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **path** | **str**| Artifact filepath. | [optional] 
 **step** | **int**| Artifact logging step. | [optional] 
 **kind** | **str**| Artifact kind. | [optional] 

### Return type

[**V1ArtifactTreeResponse**](V1ArtifactTreeResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run_logs_file**
> str get_run_logs_file(owner, project, uuid, path=path, step=step, type=type)

Get run logs get file

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
path = 'path_example' # str | Artifact filepath. (optional)
step = 56 # int | Artifact logging step. (optional)
type = 'type_example' # str | Artifact type. (optional)

try:
    # Get run logs get file
    api_response = api_instance.get_run_logs_file(owner, project, uuid, path=path, step=step, type=type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run_logs_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **path** | **str**| Artifact filepath. | [optional] 
 **step** | **int**| Artifact logging step. | [optional] 
 **type** | **str**| Artifact type. | [optional] 

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run_logs_tree**
> V1ArtifactTreeResponse get_run_logs_tree(owner, project, uuid, path=path, step=step, kind=kind)

Get run logs list

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
path = 'path_example' # str | Artifact filepath. (optional)
step = 56 # int | Artifact logging step. (optional)
kind = 'kind_example' # str | Artifact kind. (optional)

try:
    # Get run logs list
    api_response = api_instance.get_run_logs_tree(owner, project, uuid, path=path, step=step, kind=kind)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run_logs_tree: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **path** | **str**| Artifact filepath. | [optional] 
 **step** | **int**| Artifact logging step. | [optional] 
 **kind** | **str**| Artifact kind. | [optional] 

### Return type

[**V1ArtifactTreeResponse**](V1ArtifactTreeResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_run_settings**
> V1RunSettings get_run_settings(owner, project, uuid)

Get Run settings

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
    # Get Run settings
    api_response = api_instance.get_run_settings(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->get_run_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1RunSettings**](V1RunSettings.md)

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

# **impersonate_token**
> V1Auth impersonate_token(owner, project, uuid)

Impersonate run token

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
    # Impersonate run token
    api_response = api_instance.impersonate_token(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->impersonate_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1Auth**](V1Auth.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **invalidate_run**
> invalidate_run(owner, project, uuid, body)

Invalidate run

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
body = polyaxon_sdk.V1ProjectEntityResourceRequest() # V1ProjectEntityResourceRequest | 

try:
    # Invalidate run
    api_instance.invalidate_run(owner, project, uuid, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->invalidate_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1ProjectEntityResourceRequest**](V1ProjectEntityResourceRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **invalidate_runs**
> invalidate_runs(owner, project, body)

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
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

try:
    # Invalidate runs
    api_instance.invalidate_runs(owner, project, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->invalidate_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_archived_runs**
> V1ListRunsResponse list_archived_runs(user, offset=offset, limit=limit, sort=sort, query=query)

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
user = 'user_example' # str | User
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List archived runs for user
    api_response = api_instance.list_archived_runs(user, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->list_archived_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| User | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_bookmarked_runs**
> V1ListRunsResponse list_bookmarked_runs(user, offset=offset, limit=limit, sort=sort, query=query)

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
user = 'user_example' # str | User
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List bookmarked runs for user
    api_response = api_instance.list_bookmarked_runs(user, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->list_bookmarked_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| User | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_runs**
> V1ListRunsResponse list_runs(owner, project, offset=offset, limit=limit, sort=sort, query=query)

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
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List runs
    api_response = api_instance.list_runs(owner, project, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->list_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **offset** | **int**| Pagination offset. | [optional] 
 **limit** | **int**| Limit size. | [optional] 
 **sort** | **str**| Sort to order the search. | [optional] 
 **query** | **str**| Query filter the search search. | [optional] 

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
body = polyaxon_sdk.V1Run() # V1Run | Run object

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
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restart_run**
> V1Run restart_run(entity_owner, entity_project, entity_uuid, body)

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
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project where the experiement will be assigned
entity_uuid = 'entity_uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1Run() # V1Run | Run object

try:
    # Restart run
    api_response = api_instance.restart_run(entity_owner, entity_project, entity_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->restart_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project where the experiement will be assigned | 
 **entity_uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_run**
> restore_run(owner, project, uuid)

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
    api_instance.restore_run(owner, project, uuid)
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

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_run**
> V1Run resume_run(entity_owner, entity_project, entity_uuid, body)

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
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project where the experiement will be assigned
entity_uuid = 'entity_uuid_example' # str | Unique integer identifier of the entity
body = polyaxon_sdk.V1Run() # V1Run | Run object

try:
    # Resume run
    api_response = api_instance.resume_run(entity_owner, entity_project, entity_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsV1Api->resume_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project where the experiement will be assigned | 
 **entity_uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_run_tensorboard**
> start_run_tensorboard(owner, project, uuid, body)

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
body = polyaxon_sdk.V1ProjectEntityResourceRequest() # V1ProjectEntityResourceRequest | 

try:
    # Start run tensorboard
    api_instance.start_run_tensorboard(owner, project, uuid, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->start_run_tensorboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1ProjectEntityResourceRequest**](V1ProjectEntityResourceRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_run**
> stop_run(owner, project, uuid)

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

try:
    # Stop run
    api_instance.stop_run(owner, project, uuid)
except ApiException as e:
    print("Exception when calling RunsV1Api->stop_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_run_tensorboard**
> stop_run_tensorboard(owner, project, uuid)

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
    api_instance.stop_run_tensorboard(owner, project, uuid)
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

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_runs**
> stop_runs(owner, project, body)

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
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

try:
    # Stop runs
    api_instance.stop_runs(owner, project, body)
except ApiException as e:
    print("Exception when calling RunsV1Api->stop_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unbookmark_run**
> unbookmark_run(owner, project, uuid)

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
    api_instance.unbookmark_run(owner, project, uuid)
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

void (empty response body)

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
body = polyaxon_sdk.V1Run() # V1Run | Run object

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
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_run_artifact**
> upload_run_artifact(owner, project, uuid, uploadfile, path=path, overwrite=overwrite)

Upload an artifact file to a store via run access

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
project = 'project_example' # str | Project having access to the store
uuid = 'uuid_example' # str | Unique integer identifier of the entity
uploadfile = '/path/to/file.txt' # file | The file to upload.
path = 'path_example' # str | File path query params. (optional)
overwrite = true # bool | File path query params. (optional)

try:
    # Upload an artifact file to a store via run access
    api_instance.upload_run_artifact(owner, project, uuid, uploadfile, path=path, overwrite=overwrite)
except ApiException as e:
    print("Exception when calling RunsV1Api->upload_run_artifact: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project having access to the store | 
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_run_logs**
> upload_run_logs(owner, project, uuid, uploadfile, path=path, overwrite=overwrite)

Upload a logs file to a store via run access

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
project = 'project_example' # str | Project having access to the store
uuid = 'uuid_example' # str | Unique integer identifier of the entity
uploadfile = '/path/to/file.txt' # file | The file to upload.
path = 'path_example' # str | File path query params. (optional)
overwrite = true # bool | File path query params. (optional)

try:
    # Upload a logs file to a store via run access
    api_instance.upload_run_logs(owner, project, uuid, uploadfile, path=path, overwrite=overwrite)
except ApiException as e:
    print("Exception when calling RunsV1Api->upload_run_logs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project having access to the store | 
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

