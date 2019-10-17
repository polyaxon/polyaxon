# polyaxon_sdk.ProjectsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_project**](ProjectsV1Api.md#archive_project) | **POST** /api/v1/{owner}/{project}/archive | Stop run
[**bookmark_project**](ProjectsV1Api.md#bookmark_project) | **POST** /api/v1/{owner}/{project}/bookmark | Stop run
[**create_project**](ProjectsV1Api.md#create_project) | **POST** /api/v1/{owner}/projects/create | Get run
[**delete_experiment**](ProjectsV1Api.md#delete_experiment) | **DELETE** /api/v1/{owner}/projecs/{project} | Delete runs
[**disable_project_ci**](ProjectsV1Api.md#disable_project_ci) | **DELETE** /api/v1/{owner}/{project}/ci | Restart run
[**enable_project_ci**](ProjectsV1Api.md#enable_project_ci) | **POST** /api/v1/{owner}/{project}/ci | Restart run with copy
[**get_project**](ProjectsV1Api.md#get_project) | **GET** /api/v1/{owner}/projects/{project} | Update run
[**list_archived_projects**](ProjectsV1Api.md#list_archived_projects) | **GET** /api/v1/archives/{user}/projects | Create new run
[**list_bookmarked_projects**](ProjectsV1Api.md#list_bookmarked_projects) | **GET** /api/v1/bookmarks/{user}/projects | List archived runs for user
[**list_project_names**](ProjectsV1Api.md#list_project_names) | **GET** /api/v1/{owner}/projects/names | List bookmarked runs for user
[**list_projects**](ProjectsV1Api.md#list_projects) | **GET** /api/v1/{owner}/projects/list | List runs
[**patch_project**](ProjectsV1Api.md#patch_project) | **PATCH** /api/v1/{owner}/projects/{project} | Delete run
[**restore_experiment**](ProjectsV1Api.md#restore_experiment) | **POST** /api/v1/{owner}/{project}/restore | Stop runs
[**unbookmark_project**](ProjectsV1Api.md#unbookmark_project) | **DELETE** /api/v1/{owner}/{project}/unbookmark | Invalidate runs
[**update_project**](ProjectsV1Api.md#update_project) | **PUT** /api/v1/{owner}/projects/{project} | Patch run


# **archive_project**
> object archive_project(owner, project)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Stop run
    api_response = api_instance.archive_project(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->archive_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bookmark_project**
> object bookmark_project(owner, project)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Stop run
    api_response = api_instance.bookmark_project(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->bookmark_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_project**
> V1Project create_project(owner, body)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1OwnerBodyRequest() # V1OwnerBodyRequest | 

try:
    # Get run
    api_response = api_instance.create_project(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->create_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1OwnerBodyRequest**](V1OwnerBodyRequest.md)|  | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_experiment**
> object delete_experiment(owner, project)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Delete runs
    api_response = api_instance.delete_experiment(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->delete_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **disable_project_ci**
> object disable_project_ci(owner, project)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Restart run
    api_response = api_instance.disable_project_ci(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->disable_project_ci: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enable_project_ci**
> object enable_project_ci(owner, project)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Restart run with copy
    api_response = api_instance.enable_project_ci(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->enable_project_ci: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project**
> V1Project get_project(owner, project)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Update run
    api_response = api_instance.get_project(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->get_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_archived_projects**
> V1ListProjectsResponse list_archived_projects(user)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
user = 'user_example' # str | Owner of the namespace

try:
    # Create new run
    api_response = api_instance.list_archived_projects(user)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->list_archived_projects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| Owner of the namespace | 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_bookmarked_projects**
> V1ListProjectsResponse list_bookmarked_projects(user)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
user = 'user_example' # str | Owner of the namespace

try:
    # List archived runs for user
    api_response = api_instance.list_bookmarked_projects(user)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->list_bookmarked_projects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **str**| Owner of the namespace | 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_project_names**
> V1ListProjectsResponse list_project_names(owner)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace

try:
    # List bookmarked runs for user
    api_response = api_instance.list_project_names(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->list_project_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_projects**
> V1ListProjectsResponse list_projects(owner)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace

try:
    # List runs
    api_response = api_instance.list_projects(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->list_projects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_project**
> V1Project patch_project(owner, project, body)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Delete run
    api_response = api_instance.patch_project(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->patch_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restore_experiment**
> object restore_experiment(owner, project)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Stop runs
    api_response = api_instance.restore_experiment(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->restore_experiment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unbookmark_project**
> object unbookmark_project(owner, project)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce

try:
    # Invalidate runs
    api_response = api_instance.unbookmark_project(owner, project)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->unbookmark_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_project**
> V1Project update_project(owner, project, body)

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
api_instance = polyaxon_sdk.ProjectsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1ProjectBodyRequest() # V1ProjectBodyRequest | 

try:
    # Patch run
    api_response = api_instance.update_project(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsV1Api->update_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

