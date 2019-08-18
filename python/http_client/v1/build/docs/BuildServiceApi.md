# swagger_client.BuildServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_build**](BuildServiceApi.md#archive_build) | **POST** /v1/{owner}/{project}/builds/{id}/archive | Archive build
[**bookmark_build**](BuildServiceApi.md#bookmark_build) | **POST** /v1/{owner}/{project}/builds/{id}/bookmark | Bookmark build
[**create_build**](BuildServiceApi.md#create_build) | **POST** /v1/{owner}/{project}/builds | Create new build
[**create_build_status**](BuildServiceApi.md#create_build_status) | **POST** /v1/{owner}/{project}/builds/{id}/statuses | Create new build status
[**delete_build**](BuildServiceApi.md#delete_build) | **DELETE** /v1/{owner}/{project}/builds/{id} | Delete build
[**delete_builds**](BuildServiceApi.md#delete_builds) | **DELETE** /v1/{owner}/{project}/builds/delete | Delete builds
[**get_build**](BuildServiceApi.md#get_build) | **GET** /v1/{owner}/{project}/builds/{id} | Get build
[**get_build_code_ref**](BuildServiceApi.md#get_build_code_ref) | **GET** /v1/{owner}/{project}/builds/{id}/coderef | Get build code ref
[**greate_build_code_ref**](BuildServiceApi.md#greate_build_code_ref) | **POST** /v1/{entity.owner}/{entity.project}/builds/{entity.id}/coderef | Create build code ref
[**list_archived_builds**](BuildServiceApi.md#list_archived_builds) | **GET** /v1/archives/{owner}/builds | List archived builds
[**list_bookmarked_builds**](BuildServiceApi.md#list_bookmarked_builds) | **GET** /v1/bookmarks/{owner}/builds | List bookmarked builds
[**list_build_statuses**](BuildServiceApi.md#list_build_statuses) | **GET** /v1/{owner}/{project}/builds/{id}/statuses | List build statuses
[**list_builds**](BuildServiceApi.md#list_builds) | **GET** /v1/{owner}/{project}/builds | List builds
[**restart_build**](BuildServiceApi.md#restart_build) | **POST** /v1/{owner}/{project}/builds/{id}/restart | Restart build
[**restore_build**](BuildServiceApi.md#restore_build) | **POST** /v1/{owner}/{project}/builds/{id}/restore | Restore build
[**stop_build**](BuildServiceApi.md#stop_build) | **POST** /v1/{owner}/{project}/builds/{id}/stop | Stop build
[**stop_builds**](BuildServiceApi.md#stop_builds) | **POST** /v1/{owner}/{project}/builds/stop | Stop builds
[**un_bookmark_build**](BuildServiceApi.md#un_bookmark_build) | **DELETE** /v1/{owner}/{project}/builds/{id}/unbookmark | UnBookmark build
[**update_build2**](BuildServiceApi.md#update_build2) | **PUT** /v1/{owner}/{project}/builds/{build.id} | Update build


# **archive_build**
> object archive_build(owner, project, id)

Archive build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Archive build
    api_response = api_instance.archive_build(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->archive_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bookmark_build**
> object bookmark_build(owner, project, id)

Bookmark build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Bookmark build
    api_response = api_instance.bookmark_build(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->bookmark_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_build**
> V1Build create_build(owner, project, body)

Create new build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = swagger_client.V1BuildBodyRequest() # V1BuildBodyRequest | 

try:
    # Create new build
    api_response = api_instance.create_build(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->create_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **body** | [**V1BuildBodyRequest**](V1BuildBodyRequest.md)|  | 

### Return type

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_build_status**
> V1BuildStatus create_build_status(owner, project, id, body)

Create new build status

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Create new build status
    api_response = api_instance.create_build_status(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->create_build_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1BuildStatus**](V1BuildStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_build**
> object delete_build(owner, project, id)

Delete build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Delete build
    api_response = api_instance.delete_build(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->delete_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_builds**
> object delete_builds(owner, project, body)

Delete builds

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Delete builds
    api_response = api_instance.delete_builds(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->delete_builds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_build**
> V1Build get_build(owner, project, id)

Get build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Get build
    api_response = api_instance.get_build(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->get_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_build_code_ref**
> V1CodeReference get_build_code_ref(owner, project, id)

Get build code ref

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Get build code ref
    api_response = api_instance.get_build_code_ref(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->get_build_code_ref: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1CodeReference**](V1CodeReference.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **greate_build_code_ref**
> V1CodeReference greate_build_code_ref(entity_owner, entity_project, entity_id, body)

Create build code ref

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
entity_owner = 'entity_owner_example' # str | Owner of the namespace
entity_project = 'entity_project_example' # str | Project where the experiement will be assigned
entity_id = 'entity_id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1CodeReferenceBodyRequest() # V1CodeReferenceBodyRequest | 

try:
    # Create build code ref
    api_response = api_instance.greate_build_code_ref(entity_owner, entity_project, entity_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->greate_build_code_ref: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **str**| Owner of the namespace | 
 **entity_project** | **str**| Project where the experiement will be assigned | 
 **entity_id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1CodeReferenceBodyRequest**](V1CodeReferenceBodyRequest.md)|  | 

### Return type

[**V1CodeReference**](V1CodeReference.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_archived_builds**
> V1ListBuildsResponse list_archived_builds(owner)

List archived builds

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace

try:
    # List archived builds
    api_response = api_instance.list_archived_builds(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->list_archived_builds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListBuildsResponse**](V1ListBuildsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_bookmarked_builds**
> V1ListBuildsResponse list_bookmarked_builds(owner)

List bookmarked builds

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace

try:
    # List bookmarked builds
    api_response = api_instance.list_bookmarked_builds(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->list_bookmarked_builds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListBuildsResponse**](V1ListBuildsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_build_statuses**
> V1ListBuildStatusesResponse list_build_statuses(owner, project, id)

List build statuses

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # List build statuses
    api_response = api_instance.list_build_statuses(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->list_build_statuses: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1ListBuildStatusesResponse**](V1ListBuildStatusesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_builds**
> V1ListBuildsResponse list_builds(owner, project)

List builds

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # List builds
    api_response = api_instance.list_builds(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->list_builds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

[**V1ListBuildsResponse**](V1ListBuildsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restart_build**
> V1Build restart_build(owner, project, id, body)

Restart build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Restart build
    api_response = api_instance.restart_build(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->restart_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_build**
> object restore_build(owner, project, id)

Restore build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # Restore build
    api_response = api_instance.restore_build(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->restore_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_build**
> object stop_build(owner, project, id, body)

Stop build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity
body = swagger_client.V1OwnedEntityIdRequest() # V1OwnedEntityIdRequest | 

try:
    # Stop build
    api_response = api_instance.stop_build(owner, project, id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->stop_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 
 **body** | [**V1OwnedEntityIdRequest**](V1OwnedEntityIdRequest.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_builds**
> object stop_builds(owner, project, body)

Stop builds

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = swagger_client.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Stop builds
    api_response = api_instance.stop_builds(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->stop_builds: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **un_bookmark_build**
> object un_bookmark_build(owner, project, id)

UnBookmark build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
id = 'id_example' # str | Unique integer identifier of the entity

try:
    # UnBookmark build
    api_response = api_instance.un_bookmark_build(owner, project, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->un_bookmark_build: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **id** | **str**| Unique integer identifier of the entity | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_build2**
> V1Build update_build2(owner, project, build_id, body)

Update build

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BuildServiceApi()
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
build_id = 'build_id_example' # str | Unique integer identifier
body = swagger_client.V1BuildBodyRequest() # V1BuildBodyRequest | 

try:
    # Update build
    api_response = api_instance.update_build2(owner, project, build_id, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuildServiceApi->update_build2: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **build_id** | **str**| Unique integer identifier | 
 **body** | [**V1BuildBodyRequest**](V1BuildBodyRequest.md)|  | 

### Return type

[**V1Build**](V1Build.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

