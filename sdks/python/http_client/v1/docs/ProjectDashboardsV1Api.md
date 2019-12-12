# polyaxon_sdk.ProjectDashboardsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_project_dashboard**](ProjectDashboardsV1Api.md#create_project_dashboard) | **POST** /api/v1/{owner}/{project}/dashboards | List runs
[**delete_project_dashboard**](ProjectDashboardsV1Api.md#delete_project_dashboard) | **DELETE** /api/v1/{owner}/{project}/dashboards/{uuid} | Patch run
[**get_project_dashboard**](ProjectDashboardsV1Api.md#get_project_dashboard) | **GET** /api/v1/{owner}/{project}/dashboards/{uuid} | Create new run
[**list_project_dashboard_names**](ProjectDashboardsV1Api.md#list_project_dashboard_names) | **GET** /api/v1/{owner}/{project}/dashboards/names | List bookmarked runs for user
[**list_project_dashboards**](ProjectDashboardsV1Api.md#list_project_dashboards) | **GET** /api/v1/{owner}/{project}/dashboards | List archived runs for user
[**patch_project_dashboard**](ProjectDashboardsV1Api.md#patch_project_dashboard) | **PATCH** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Update run
[**promote_project_dashboard**](ProjectDashboardsV1Api.md#promote_project_dashboard) | **POST** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid}/promote | Delete run
[**update_project_dashboard**](ProjectDashboardsV1Api.md#update_project_dashboard) | **PUT** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Get run


# **create_project_dashboard**
> V1Dashboard create_project_dashboard(owner, project, body)

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
api_instance = polyaxon_sdk.ProjectDashboardsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
body = polyaxon_sdk.V1Dashboard() # V1Dashboard | Dashboard body

try:
    # List runs
    api_response = api_instance.create_project_dashboard(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->create_project_dashboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_project_dashboard**
> delete_project_dashboard(owner, project, uuid)

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
api_instance = polyaxon_sdk.ProjectDashboardsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Patch run
    api_instance.delete_project_dashboard(owner, project, uuid)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->delete_project_dashboard: %s\n" % e)
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

# **get_project_dashboard**
> V1Dashboard get_project_dashboard(owner, project, uuid)

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
api_instance = polyaxon_sdk.ProjectDashboardsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project where the experiement will be assigned
uuid = 'uuid_example' # str | Unique integer identifier of the entity

try:
    # Create new run
    api_response = api_instance.get_project_dashboard(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->get_project_dashboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project where the experiement will be assigned | 
 **uuid** | **str**| Unique integer identifier of the entity | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_project_dashboard_names**
> V1ListDashboardsResponse list_project_dashboard_names(owner, project, offset=offset, limit=limit, sort=sort, query=query)

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
api_instance = polyaxon_sdk.ProjectDashboardsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List bookmarked runs for user
    api_response = api_instance.list_project_dashboard_names(owner, project, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->list_project_dashboard_names: %s\n" % e)
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

[**V1ListDashboardsResponse**](V1ListDashboardsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_project_dashboards**
> V1ListDashboardsResponse list_project_dashboards(owner, project, offset=offset, limit=limit, sort=sort, query=query)

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
api_instance = polyaxon_sdk.ProjectDashboardsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List archived runs for user
    api_response = api_instance.list_project_dashboards(owner, project, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->list_project_dashboards: %s\n" % e)
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

[**V1ListDashboardsResponse**](V1ListDashboardsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_project_dashboard**
> V1Dashboard patch_project_dashboard(owner, project, dashboard_uuid, body)

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
api_instance = polyaxon_sdk.ProjectDashboardsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
dashboard_uuid = 'dashboard_uuid_example' # str | UUID
body = polyaxon_sdk.V1Dashboard() # V1Dashboard | Dashboard body

try:
    # Update run
    api_response = api_instance.patch_project_dashboard(owner, project, dashboard_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->patch_project_dashboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **dashboard_uuid** | **str**| UUID | 
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **promote_project_dashboard**
> V1Dashboard promote_project_dashboard(owner, project, dashboard_uuid)

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
api_instance = polyaxon_sdk.ProjectDashboardsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
dashboard_uuid = 'dashboard_uuid_example' # str | UUID

try:
    # Delete run
    api_response = api_instance.promote_project_dashboard(owner, project, dashboard_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->promote_project_dashboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **dashboard_uuid** | **str**| UUID | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_project_dashboard**
> V1Dashboard update_project_dashboard(owner, project, dashboard_uuid, body)

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
api_instance = polyaxon_sdk.ProjectDashboardsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
project = 'project_example' # str | Project under namesapce
dashboard_uuid = 'dashboard_uuid_example' # str | UUID
body = polyaxon_sdk.V1Dashboard() # V1Dashboard | Dashboard body

try:
    # Get run
    api_response = api_instance.update_project_dashboard(owner, project, dashboard_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->update_project_dashboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project under namesapce | 
 **dashboard_uuid** | **str**| UUID | 
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

