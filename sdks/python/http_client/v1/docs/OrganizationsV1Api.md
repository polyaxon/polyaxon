# polyaxon_sdk.OrganizationsV1Api
Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approve_organization_runs**](OrganizationsV1Api.md#approve_organization_runs) | **POST** /api/v1/orgs/{owner}/runs/approve | Approve cross-project runs selection
[**archive_organization_runs**](OrganizationsV1Api.md#archive_organization_runs) | **POST** /api/v1/orgs/{owner}/runs/archive | Archive cross-project runs selection
[**bookmark_organization_runs**](OrganizationsV1Api.md#bookmark_organization_runs) | **POST** /api/v1/orgs/{owner}/runs/bookmark | Bookmark cross-project runs selection
[**create_organization**](OrganizationsV1Api.md#create_organization) | **POST** /api/v1/orgs/create | Create organization
[**create_organization_member**](OrganizationsV1Api.md#create_organization_member) | **POST** /api/v1/orgs/{owner}/members | Create organization member
[**delete_organization**](OrganizationsV1Api.md#delete_organization) | **DELETE** /api/v1/orgs/{owner} | Delete organization
[**delete_organization_invitation**](OrganizationsV1Api.md#delete_organization_invitation) | **DELETE** /api/v1/orgs/{owner}/invitations | Delete organization invitation details
[**delete_organization_member**](OrganizationsV1Api.md#delete_organization_member) | **DELETE** /api/v1/orgs/{owner}/members/{name} | Delete organization member details
[**delete_organization_runs**](OrganizationsV1Api.md#delete_organization_runs) | **DELETE** /api/v1/orgs/{owner}/runs/delete | Delete cross-project runs selection
[**get_organization**](OrganizationsV1Api.md#get_organization) | **GET** /api/v1/orgs/{owner} | Get organization
[**get_organization_activities**](OrganizationsV1Api.md#get_organization_activities) | **GET** /api/v1/orgs/{owner}/activities | Get organization activities
[**get_organization_invitation**](OrganizationsV1Api.md#get_organization_invitation) | **GET** /api/v1/orgs/{owner}/invitations | Get organization invitation details
[**get_organization_member**](OrganizationsV1Api.md#get_organization_member) | **GET** /api/v1/orgs/{owner}/members/{name} | Get organization member details
[**get_organization_runs**](OrganizationsV1Api.md#get_organization_runs) | **GET** /api/v1/orgs/{owner}/runs | Get all runs in an organization
[**get_organization_settings**](OrganizationsV1Api.md#get_organization_settings) | **GET** /api/v1/orgs/{owner}/settings | Get organization settings
[**get_organization_stats**](OrganizationsV1Api.md#get_organization_stats) | **GET** /api/v1/orgs/{owner}/stats | Get organization stats
[**invalidate_organization_runs**](OrganizationsV1Api.md#invalidate_organization_runs) | **POST** /api/v1/orgs/{owner}/runs/invalidate | Invalidate cross-project runs selection
[**list_organization_member_names**](OrganizationsV1Api.md#list_organization_member_names) | **GET** /api/v1/orgs/{owner}/members/names | Get organization member names
[**list_organization_members**](OrganizationsV1Api.md#list_organization_members) | **GET** /api/v1/orgs/{owner}/members | Get organization members
[**list_organization_names**](OrganizationsV1Api.md#list_organization_names) | **GET** /api/v1/orgs/names | List organizations names
[**list_organizations**](OrganizationsV1Api.md#list_organizations) | **GET** /api/v1/orgs/list | List organizations
[**organization_plan**](OrganizationsV1Api.md#organization_plan) | **POST** /api/v1/orgs/{owner}/plan | Organization plan
[**patch_organization**](OrganizationsV1Api.md#patch_organization) | **PATCH** /api/v1/orgs/{owner} | Patch organization
[**patch_organization_invitation**](OrganizationsV1Api.md#patch_organization_invitation) | **PATCH** /api/v1/orgs/{owner}/invitations | Patch organization invitation
[**patch_organization_member**](OrganizationsV1Api.md#patch_organization_member) | **PATCH** /api/v1/orgs/{owner}/members/{member.user} | Patch organization member
[**patch_organization_settings**](OrganizationsV1Api.md#patch_organization_settings) | **PATCH** /api/v1/orgs/{owner}/settings | Patch oranization settings
[**resend_organization_invitation**](OrganizationsV1Api.md#resend_organization_invitation) | **POST** /api/v1/orgs/{owner}/invitations | Resend organization invitation
[**restore_organization_runs**](OrganizationsV1Api.md#restore_organization_runs) | **POST** /api/v1/orgs/{owner}/runs/restore | Restore cross-project runs selection
[**stop_organization_runs**](OrganizationsV1Api.md#stop_organization_runs) | **POST** /api/v1/orgs/{owner}/runs/stop | Stop cross-project runs selection
[**tag_organization_runs**](OrganizationsV1Api.md#tag_organization_runs) | **POST** /api/v1/orgs/{owner}/runs/tag | Tag cross-project runs selection
[**transfer_organization_runs**](OrganizationsV1Api.md#transfer_organization_runs) | **POST** /api/v1/orgs/{owner}/runs/transfer | Transfer cross-project runs selection to a new project
[**update_organization**](OrganizationsV1Api.md#update_organization) | **PUT** /api/v1/orgs/{owner} | Update organization
[**update_organization_invitation**](OrganizationsV1Api.md#update_organization_invitation) | **PUT** /api/v1/orgs/{owner}/invitations | Update organization invitation
[**update_organization_member**](OrganizationsV1Api.md#update_organization_member) | **PUT** /api/v1/orgs/{owner}/members/{member.user} | Update organization member
[**update_organization_settings**](OrganizationsV1Api.md#update_organization_settings) | **PUT** /api/v1/orgs/{owner}/settings | Update organization settings


# **approve_organization_runs**
> approve_organization_runs(owner, body)

Approve cross-project runs selection

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

    try:
        # Approve cross-project runs selection
        api_instance.approve_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->approve_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

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

# **archive_organization_runs**
> archive_organization_runs(owner, body)

Archive cross-project runs selection

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

    try:
        # Archive cross-project runs selection
        api_instance.archive_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->archive_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

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

# **bookmark_organization_runs**
> bookmark_organization_runs(owner, body)

Bookmark cross-project runs selection

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

    try:
        # Bookmark cross-project runs selection
        api_instance.bookmark_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->bookmark_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

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

# **create_organization**
> V1Organization create_organization(body)

Create organization

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    body = polyaxon_sdk.V1Organization() # V1Organization | 

    try:
        # Create organization
        api_response = api_instance.create_organization(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->create_organization: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**V1Organization**](V1Organization.md)|  | 

### Return type

[**V1Organization**](V1Organization.md)

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

# **create_organization_member**
> V1OrganizationMember create_organization_member(owner, body, email=email)

Create organization member

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body
email = 'email_example' # str | Optional email. (optional)

    try:
        # Create organization member
        api_response = api_instance.create_organization_member(owner, body, email=email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->create_organization_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **str**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

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

# **delete_organization**
> delete_organization(owner, usage=usage)

Delete organization

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
usage = 'usage_example' # str | Owner usage query param. (optional)

    try:
        # Delete organization
        api_instance.delete_organization(owner, usage=usage)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->delete_organization: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **usage** | **str**| Owner usage query param. | [optional] 

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

# **delete_organization_invitation**
> delete_organization_invitation(owner, member_user=member_user, member_user_email=member_user_email, member_role=member_role, member_created_at=member_created_at, member_updated_at=member_updated_at, email=email)

Delete organization invitation details

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
member_user = 'member_user_example' # str | User. (optional)
member_user_email = 'member_user_email_example' # str | Read-only User email. (optional)
member_role = 'member_role_example' # str | Role. (optional)
member_created_at = '2013-10-20T19:20:30+01:00' # datetime | Optional time when the entity was created. (optional)
member_updated_at = '2013-10-20T19:20:30+01:00' # datetime | Optional last time the entity was updated. (optional)
email = 'email_example' # str | Optional email. (optional)

    try:
        # Delete organization invitation details
        api_instance.delete_organization_invitation(owner, member_user=member_user, member_user_email=member_user_email, member_role=member_role, member_created_at=member_created_at, member_updated_at=member_updated_at, email=email)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->delete_organization_invitation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **member_user** | **str**| User. | [optional] 
 **member_user_email** | **str**| Read-only User email. | [optional] 
 **member_role** | **str**| Role. | [optional] 
 **member_created_at** | **datetime**| Optional time when the entity was created. | [optional] 
 **member_updated_at** | **datetime**| Optional last time the entity was updated. | [optional] 
 **email** | **str**| Optional email. | [optional] 

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

# **delete_organization_member**
> delete_organization_member(owner, name)

Delete organization member details

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
name = 'name_example' # str | Component under namesapce

    try:
        # Delete organization member details
        api_instance.delete_organization_member(owner, name)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->delete_organization_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **name** | **str**| Component under namesapce | 

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

# **delete_organization_runs**
> delete_organization_runs(owner, body)

Delete cross-project runs selection

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

    try:
        # Delete cross-project runs selection
        api_instance.delete_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->delete_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

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

# **get_organization**
> V1Organization get_organization(owner, usage=usage)

Get organization

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
usage = 'usage_example' # str | Owner usage query param. (optional)

    try:
        # Get organization
        api_response = api_instance.get_organization(owner, usage=usage)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->get_organization: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **usage** | **str**| Owner usage query param. | [optional] 

### Return type

[**V1Organization**](V1Organization.md)

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

# **get_organization_activities**
> V1ListActivitiesResponse get_organization_activities(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)

Get organization activities

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
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
        # Get organization activities
        api_response = api_instance.get_organization_activities(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->get_organization_activities: %s\n" % e)
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

[**V1ListActivitiesResponse**](V1ListActivitiesResponse.md)

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

# **get_organization_invitation**
> V1OrganizationMember get_organization_invitation(owner, member_user=member_user, member_user_email=member_user_email, member_role=member_role, member_created_at=member_created_at, member_updated_at=member_updated_at, email=email)

Get organization invitation details

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
member_user = 'member_user_example' # str | User. (optional)
member_user_email = 'member_user_email_example' # str | Read-only User email. (optional)
member_role = 'member_role_example' # str | Role. (optional)
member_created_at = '2013-10-20T19:20:30+01:00' # datetime | Optional time when the entity was created. (optional)
member_updated_at = '2013-10-20T19:20:30+01:00' # datetime | Optional last time the entity was updated. (optional)
email = 'email_example' # str | Optional email. (optional)

    try:
        # Get organization invitation details
        api_response = api_instance.get_organization_invitation(owner, member_user=member_user, member_user_email=member_user_email, member_role=member_role, member_created_at=member_created_at, member_updated_at=member_updated_at, email=email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->get_organization_invitation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **member_user** | **str**| User. | [optional] 
 **member_user_email** | **str**| Read-only User email. | [optional] 
 **member_role** | **str**| Role. | [optional] 
 **member_created_at** | **datetime**| Optional time when the entity was created. | [optional] 
 **member_updated_at** | **datetime**| Optional last time the entity was updated. | [optional] 
 **email** | **str**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

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

# **get_organization_member**
> V1OrganizationMember get_organization_member(owner, name)

Get organization member details

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
name = 'name_example' # str | Component under namesapce

    try:
        # Get organization member details
        api_response = api_instance.get_organization_member(owner, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->get_organization_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **name** | **str**| Component under namesapce | 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

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

# **get_organization_runs**
> V1ListRunsResponse get_organization_runs(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)

Get all runs in an organization

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
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
        # Get all runs in an organization
        api_response = api_instance.get_organization_runs(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->get_organization_runs: %s\n" % e)
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

[**V1ListRunsResponse**](V1ListRunsResponse.md)

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

# **get_organization_settings**
> V1Organization get_organization_settings(owner, organization_user=organization_user, organization_user_email=organization_user_email, organization_name=organization_name, organization_is_public=organization_is_public, organization_created_at=organization_created_at, organization_updated_at=organization_updated_at, organization_support_revoke_at=organization_support_revoke_at, organization_expiration=organization_expiration, organization_role=organization_role, organization_queue=organization_queue, organization_preset=organization_preset, organization_is_cloud_viewable=organization_is_cloud_viewable)

Get organization settings

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
organization_user = 'organization_user_example' # str | User. (optional)
organization_user_email = 'organization_user_email_example' # str | Read-only User email. (optional)
organization_name = 'organization_name_example' # str | Name. (optional)
organization_is_public = True # bool | Optional flag to tell if this organization is public. (optional)
organization_created_at = '2013-10-20T19:20:30+01:00' # datetime | Optional time when the entity was created. (optional)
organization_updated_at = '2013-10-20T19:20:30+01:00' # datetime | Optional last time the entity was updated. (optional)
organization_support_revoke_at = '2013-10-20T19:20:30+01:00' # datetime | Optional time to revoke support access. (optional)
organization_expiration = 56 # int | Optional expiration for support. (optional)
organization_role = 'organization_role_example' # str | Current user's role in this org. (optional)
organization_queue = 'organization_queue_example' # str | Default queue. (optional)
organization_preset = 'organization_preset_example' # str | Default preset. (optional)
organization_is_cloud_viewable = True # bool | Setting to enable viewable metadata on cloud. (optional)

    try:
        # Get organization settings
        api_response = api_instance.get_organization_settings(owner, organization_user=organization_user, organization_user_email=organization_user_email, organization_name=organization_name, organization_is_public=organization_is_public, organization_created_at=organization_created_at, organization_updated_at=organization_updated_at, organization_support_revoke_at=organization_support_revoke_at, organization_expiration=organization_expiration, organization_role=organization_role, organization_queue=organization_queue, organization_preset=organization_preset, organization_is_cloud_viewable=organization_is_cloud_viewable)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->get_organization_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **organization_user** | **str**| User. | [optional] 
 **organization_user_email** | **str**| Read-only User email. | [optional] 
 **organization_name** | **str**| Name. | [optional] 
 **organization_is_public** | **bool**| Optional flag to tell if this organization is public. | [optional] 
 **organization_created_at** | **datetime**| Optional time when the entity was created. | [optional] 
 **organization_updated_at** | **datetime**| Optional last time the entity was updated. | [optional] 
 **organization_support_revoke_at** | **datetime**| Optional time to revoke support access. | [optional] 
 **organization_expiration** | **int**| Optional expiration for support. | [optional] 
 **organization_role** | **str**| Current user&#39;s role in this org. | [optional] 
 **organization_queue** | **str**| Default queue. | [optional] 
 **organization_preset** | **str**| Default preset. | [optional] 
 **organization_is_cloud_viewable** | **bool**| Setting to enable viewable metadata on cloud. | [optional] 

### Return type

[**V1Organization**](V1Organization.md)

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

# **get_organization_stats**
> object get_organization_stats(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, kind=kind, aggregate=aggregate, groupby=groupby, trunc=trunc)

Get organization stats

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search. (optional)
bookmarks = True # bool | Filter by bookmarks. (optional)
kind = 'kind_example' # str | Stats Kind. (optional)
aggregate = 'aggregate_example' # str | Stats aggregate. (optional)
groupby = 'groupby_example' # str | Stats group. (optional)
trunc = 'trunc_example' # str | Stats trunc. (optional)

    try:
        # Get organization stats
        api_response = api_instance.get_organization_stats(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, kind=kind, aggregate=aggregate, groupby=groupby, trunc=trunc)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->get_organization_stats: %s\n" % e)
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
 **kind** | **str**| Stats Kind. | [optional] 
 **aggregate** | **str**| Stats aggregate. | [optional] 
 **groupby** | **str**| Stats group. | [optional] 
 **trunc** | **str**| Stats trunc. | [optional] 

### Return type

**object**

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

# **invalidate_organization_runs**
> invalidate_organization_runs(owner, body)

Invalidate cross-project runs selection

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

    try:
        # Invalidate cross-project runs selection
        api_instance.invalidate_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->invalidate_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

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

# **list_organization_member_names**
> V1ListOrganizationMembersResponse list_organization_member_names(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)

Get organization member names

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
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
        # Get organization member names
        api_response = api_instance.list_organization_member_names(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->list_organization_member_names: %s\n" % e)
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

[**V1ListOrganizationMembersResponse**](V1ListOrganizationMembersResponse.md)

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

# **list_organization_members**
> V1ListOrganizationMembersResponse list_organization_members(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)

Get organization members

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
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
        # Get organization members
        api_response = api_instance.list_organization_members(owner, offset=offset, limit=limit, sort=sort, query=query, bookmarks=bookmarks, pins=pins, mode=mode, no_page=no_page)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->list_organization_members: %s\n" % e)
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

[**V1ListOrganizationMembersResponse**](V1ListOrganizationMembersResponse.md)

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

# **list_organization_names**
> V1ListOrganizationsResponse list_organization_names()

List organizations names

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    
    try:
        # List organizations names
        api_response = api_instance.list_organization_names()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->list_organization_names: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1ListOrganizationsResponse**](V1ListOrganizationsResponse.md)

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

# **list_organizations**
> V1ListOrganizationsResponse list_organizations()

List organizations

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    
    try:
        # List organizations
        api_response = api_instance.list_organizations()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->list_organizations: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1ListOrganizationsResponse**](V1ListOrganizationsResponse.md)

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

# **organization_plan**
> V1Organization organization_plan(owner, body)

Organization plan

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Organization() # V1Organization | Organization body

    try:
        # Organization plan
        api_response = api_instance.organization_plan(owner, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->organization_plan: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Organization**](V1Organization.md)| Organization body | 

### Return type

[**V1Organization**](V1Organization.md)

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

# **patch_organization**
> V1Organization patch_organization(owner, body)

Patch organization

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Organization() # V1Organization | Organization body

    try:
        # Patch organization
        api_response = api_instance.patch_organization(owner, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->patch_organization: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Organization**](V1Organization.md)| Organization body | 

### Return type

[**V1Organization**](V1Organization.md)

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

# **patch_organization_invitation**
> V1OrganizationMember patch_organization_invitation(owner, body, email=email)

Patch organization invitation

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body
email = 'email_example' # str | Optional email. (optional)

    try:
        # Patch organization invitation
        api_response = api_instance.patch_organization_invitation(owner, body, email=email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->patch_organization_invitation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **str**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

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

# **patch_organization_member**
> V1OrganizationMember patch_organization_member(owner, member_user, body, email=email)

Patch organization member

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
member_user = 'member_user_example' # str | User
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body
email = 'email_example' # str | Optional email. (optional)

    try:
        # Patch organization member
        api_response = api_instance.patch_organization_member(owner, member_user, body, email=email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->patch_organization_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **member_user** | **str**| User | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **str**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

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

# **patch_organization_settings**
> V1Organization patch_organization_settings(owner, body)

Patch oranization settings

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Organization() # V1Organization | Organization body

    try:
        # Patch oranization settings
        api_response = api_instance.patch_organization_settings(owner, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->patch_organization_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Organization**](V1Organization.md)| Organization body | 

### Return type

[**V1Organization**](V1Organization.md)

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

# **resend_organization_invitation**
> V1OrganizationMember resend_organization_invitation(owner, body, email=email)

Resend organization invitation

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body
email = 'email_example' # str | Optional email. (optional)

    try:
        # Resend organization invitation
        api_response = api_instance.resend_organization_invitation(owner, body, email=email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->resend_organization_invitation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **str**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

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

# **restore_organization_runs**
> restore_organization_runs(owner, body)

Restore cross-project runs selection

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

    try:
        # Restore cross-project runs selection
        api_instance.restore_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->restore_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

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

# **stop_organization_runs**
> stop_organization_runs(owner, body)

Stop cross-project runs selection

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Uuids() # V1Uuids | Uuids of the entities

    try:
        # Stop cross-project runs selection
        api_instance.stop_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->stop_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

void (empty response body)

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

# **tag_organization_runs**
> tag_organization_runs(owner, body)

Tag cross-project runs selection

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1EntitiesTags() # V1EntitiesTags | Data

    try:
        # Tag cross-project runs selection
        api_instance.tag_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->tag_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1EntitiesTags**](V1EntitiesTags.md)| Data | 

### Return type

void (empty response body)

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

# **transfer_organization_runs**
> transfer_organization_runs(owner, body)

Transfer cross-project runs selection to a new project

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1EntitiesTransfer() # V1EntitiesTransfer | Data

    try:
        # Transfer cross-project runs selection to a new project
        api_instance.transfer_organization_runs(owner, body)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->transfer_organization_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1EntitiesTransfer**](V1EntitiesTransfer.md)| Data | 

### Return type

void (empty response body)

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

# **update_organization**
> V1Organization update_organization(owner, body)

Update organization

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Organization() # V1Organization | Organization body

    try:
        # Update organization
        api_response = api_instance.update_organization(owner, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->update_organization: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Organization**](V1Organization.md)| Organization body | 

### Return type

[**V1Organization**](V1Organization.md)

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

# **update_organization_invitation**
> V1OrganizationMember update_organization_invitation(owner, body, email=email)

Update organization invitation

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body
email = 'email_example' # str | Optional email. (optional)

    try:
        # Update organization invitation
        api_response = api_instance.update_organization_invitation(owner, body, email=email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->update_organization_invitation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **str**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

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

# **update_organization_member**
> V1OrganizationMember update_organization_member(owner, member_user, body, email=email)

Update organization member

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
member_user = 'member_user_example' # str | User
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body
email = 'email_example' # str | Optional email. (optional)

    try:
        # Update organization member
        api_response = api_instance.update_organization_member(owner, member_user, body, email=email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->update_organization_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **member_user** | **str**| User | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **str**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

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

# **update_organization_settings**
> V1Organization update_organization_settings(owner, body)

Update organization settings

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
    api_instance = polyaxon_sdk.OrganizationsV1Api(api_client)
    owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Organization() # V1Organization | Organization body

    try:
        # Update organization settings
        api_response = api_instance.update_organization_settings(owner, body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganizationsV1Api->update_organization_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Organization**](V1Organization.md)| Organization body | 

### Return type

[**V1Organization**](V1Organization.md)

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

