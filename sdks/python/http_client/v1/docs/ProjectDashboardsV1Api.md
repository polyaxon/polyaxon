# polyaxon_sdk.ProjectDashboardsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**project_dashboards_v1_create_project_dashboard**](ProjectDashboardsV1Api.md#project_dashboards_v1_create_project_dashboard) | **POST** /api/v1/{owner}/{project}/dashboards | Create project dashboard
[**project_dashboards_v1_delete_project_dashboard**](ProjectDashboardsV1Api.md#project_dashboards_v1_delete_project_dashboard) | **DELETE** /api/v1/{owner}/{project}/dashboards/{uuid} | Delete project dashboard
[**project_dashboards_v1_get_project_dashboard**](ProjectDashboardsV1Api.md#project_dashboards_v1_get_project_dashboard) | **GET** /api/v1/{owner}/{project}/dashboards/{uuid} | Get project dashboard
[**project_dashboards_v1_list_project_dashboard_names**](ProjectDashboardsV1Api.md#project_dashboards_v1_list_project_dashboard_names) | **GET** /api/v1/{owner}/{project}/dashboards/names | List project dashboard
[**project_dashboards_v1_list_project_dashboards**](ProjectDashboardsV1Api.md#project_dashboards_v1_list_project_dashboards) | **GET** /api/v1/{owner}/{project}/dashboards | List project dashboards
[**project_dashboards_v1_patch_project_dashboard**](ProjectDashboardsV1Api.md#project_dashboards_v1_patch_project_dashboard) | **PATCH** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Patch project dashboard
[**project_dashboards_v1_promote_project_dashboard**](ProjectDashboardsV1Api.md#project_dashboards_v1_promote_project_dashboard) | **POST** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid}/promote | Promote project dashboard
[**project_dashboards_v1_update_project_dashboard**](ProjectDashboardsV1Api.md#project_dashboards_v1_update_project_dashboard) | **PUT** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Update project dashboard


# **project_dashboards_v1_create_project_dashboard**
> V1Dashboard project_dashboards_v1_create_project_dashboard(owner, project, body)

Create project dashboard

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
    # Create project dashboard
    api_response = api_instance.project_dashboards_v1_create_project_dashboard(owner, project, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->project_dashboards_v1_create_project_dashboard: %s\n" % e)
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

# **project_dashboards_v1_delete_project_dashboard**
> project_dashboards_v1_delete_project_dashboard(owner, project, uuid)

Delete project dashboard

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
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Delete project dashboard
    api_instance.project_dashboards_v1_delete_project_dashboard(owner, project, uuid)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->project_dashboards_v1_delete_project_dashboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **project_dashboards_v1_get_project_dashboard**
> V1Dashboard project_dashboards_v1_get_project_dashboard(owner, project, uuid)

Get project dashboard

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
project = 'project_example' # str | Project
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get project dashboard
    api_response = api_instance.project_dashboards_v1_get_project_dashboard(owner, project, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->project_dashboards_v1_get_project_dashboard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **project** | **str**| Project | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **project_dashboards_v1_list_project_dashboard_names**
> V1ListDashboardsResponse project_dashboards_v1_list_project_dashboard_names(owner, project, offset=offset, limit=limit, sort=sort, query=query)

List project dashboard

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
    # List project dashboard
    api_response = api_instance.project_dashboards_v1_list_project_dashboard_names(owner, project, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->project_dashboards_v1_list_project_dashboard_names: %s\n" % e)
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

# **project_dashboards_v1_list_project_dashboards**
> V1ListDashboardsResponse project_dashboards_v1_list_project_dashboards(owner, project, offset=offset, limit=limit, sort=sort, query=query)

List project dashboards

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
    # List project dashboards
    api_response = api_instance.project_dashboards_v1_list_project_dashboards(owner, project, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->project_dashboards_v1_list_project_dashboards: %s\n" % e)
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

# **project_dashboards_v1_patch_project_dashboard**
> V1Dashboard project_dashboards_v1_patch_project_dashboard(owner, project, dashboard_uuid, body)

Patch project dashboard

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
    # Patch project dashboard
    api_response = api_instance.project_dashboards_v1_patch_project_dashboard(owner, project, dashboard_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->project_dashboards_v1_patch_project_dashboard: %s\n" % e)
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

# **project_dashboards_v1_promote_project_dashboard**
> V1Dashboard project_dashboards_v1_promote_project_dashboard(owner, project, dashboard_uuid)

Promote project dashboard

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
    # Promote project dashboard
    api_response = api_instance.project_dashboards_v1_promote_project_dashboard(owner, project, dashboard_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->project_dashboards_v1_promote_project_dashboard: %s\n" % e)
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

# **project_dashboards_v1_update_project_dashboard**
> V1Dashboard project_dashboards_v1_update_project_dashboard(owner, project, dashboard_uuid, body)

Update project dashboard

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
    # Update project dashboard
    api_response = api_instance.project_dashboards_v1_update_project_dashboard(owner, project, dashboard_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectDashboardsV1Api->project_dashboards_v1_update_project_dashboard: %s\n" % e)
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

