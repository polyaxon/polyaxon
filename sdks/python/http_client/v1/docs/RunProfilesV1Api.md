# polyaxon_sdk.RunProfilesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_run_profile**](RunProfilesV1Api.md#create_run_profile) | **POST** /api/v1/orgs/{owner}/run_profiles | Create hub component
[**delete_run_profile**](RunProfilesV1Api.md#delete_run_profile) | **DELETE** /api/v1/orgs/{owner}/run_profiles/{uuid} | Delete hub component
[**get_run_profile**](RunProfilesV1Api.md#get_run_profile) | **GET** /api/v1/orgs/{owner}/run_profiles/{uuid} | Get hub component
[**list_run_profile_names**](RunProfilesV1Api.md#list_run_profile_names) | **GET** /api/v1/orgs/{owner}/run_profiles/names | List hub component names
[**list_run_profiles**](RunProfilesV1Api.md#list_run_profiles) | **GET** /api/v1/orgs/{owner}/run_profiles | List hub components
[**patch_run_profile**](RunProfilesV1Api.md#patch_run_profile) | **PATCH** /api/v1/orgs/{owner}/run_profiles/{run_profile.uuid} | Patch hub component
[**update_run_profile**](RunProfilesV1Api.md#update_run_profile) | **PUT** /api/v1/orgs/{owner}/run_profiles/{run_profile.uuid} | Update hub component


# **create_run_profile**
> V1RunProfile create_run_profile(owner, body)

Create hub component

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
api_instance = polyaxon_sdk.RunProfilesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1RunProfile() # V1RunProfile | Artifact store body

try:
    # Create hub component
    api_response = api_instance.create_run_profile(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunProfilesV1Api->create_run_profile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body | 

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_run_profile**
> delete_run_profile(owner, uuid)

Delete hub component

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
api_instance = polyaxon_sdk.RunProfilesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Delete hub component
    api_instance.delete_run_profile(owner, uuid)
except ApiException as e:
    print("Exception when calling RunProfilesV1Api->delete_run_profile: %s\n" % e)
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

# **get_run_profile**
> V1RunProfile get_run_profile(owner, uuid)

Get hub component

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
api_instance = polyaxon_sdk.RunProfilesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
uuid = 'uuid_example' # str | Uuid identifier of the entity

try:
    # Get hub component
    api_response = api_instance.get_run_profile(owner, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunProfilesV1Api->get_run_profile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **uuid** | **str**| Uuid identifier of the entity | 

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_run_profile_names**
> V1ListRunProfilesResponse list_run_profile_names(owner, offset=offset, limit=limit, sort=sort, query=query)

List hub component names

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
api_instance = polyaxon_sdk.RunProfilesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List hub component names
    api_response = api_instance.list_run_profile_names(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunProfilesV1Api->list_run_profile_names: %s\n" % e)
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

[**V1ListRunProfilesResponse**](V1ListRunProfilesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_run_profiles**
> V1ListRunProfilesResponse list_run_profiles(owner, offset=offset, limit=limit, sort=sort, query=query)

List hub components

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
api_instance = polyaxon_sdk.RunProfilesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List hub components
    api_response = api_instance.list_run_profiles(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunProfilesV1Api->list_run_profiles: %s\n" % e)
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

[**V1ListRunProfilesResponse**](V1ListRunProfilesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_run_profile**
> V1RunProfile patch_run_profile(owner, run_profile_uuid, body)

Patch hub component

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
api_instance = polyaxon_sdk.RunProfilesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
run_profile_uuid = 'run_profile_uuid_example' # str | UUID
body = polyaxon_sdk.V1RunProfile() # V1RunProfile | Artifact store body

try:
    # Patch hub component
    api_response = api_instance.patch_run_profile(owner, run_profile_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunProfilesV1Api->patch_run_profile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **run_profile_uuid** | **str**| UUID | 
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body | 

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_run_profile**
> V1RunProfile update_run_profile(owner, run_profile_uuid, body)

Update hub component

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
api_instance = polyaxon_sdk.RunProfilesV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
run_profile_uuid = 'run_profile_uuid_example' # str | UUID
body = polyaxon_sdk.V1RunProfile() # V1RunProfile | Artifact store body

try:
    # Update hub component
    api_response = api_instance.update_run_profile(owner, run_profile_uuid, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunProfilesV1Api->update_run_profile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **run_profile_uuid** | **str**| UUID | 
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body | 

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

