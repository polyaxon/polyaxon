# polyaxon_sdk.OrganizationsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_organization**](OrganizationsV1Api.md#create_organization) | **POST** /api/v1/organizations/create | List runs
[**create_organization_member**](OrganizationsV1Api.md#create_organization_member) | **POST** /api/v1/organizations/{owner}/members | Delete runs
[**delete_organization**](OrganizationsV1Api.md#delete_organization) | **DELETE** /api/v1/organizations/{owner} | Patch run
[**delete_organization_member**](OrganizationsV1Api.md#delete_organization_member) | **DELETE** /api/v1/organizations/{owner}/members/{member.user} | Invalidate runs
[**get_organization**](OrganizationsV1Api.md#get_organization) | **GET** /api/v1/organizations/{owner} | Create new run
[**get_organization_member**](OrganizationsV1Api.md#get_organization_member) | **GET** /api/v1/organizations/{owner}/members/{member.user} | Stop run
[**list_organization_members**](OrganizationsV1Api.md#list_organization_members) | **GET** /api/v1/organizations/{owner}/members | Delete run
[**list_organization_names**](OrganizationsV1Api.md#list_organization_names) | **GET** /api/v1/organizations/names | List bookmarked runs for user
[**list_organizations**](OrganizationsV1Api.md#list_organizations) | **GET** /api/v1/organizations/list | List archived runs for user
[**patch_organization**](OrganizationsV1Api.md#patch_organization) | **PATCH** /api/v1/organizations/{owner} | Update run
[**patch_organization_member**](OrganizationsV1Api.md#patch_organization_member) | **PATCH** /api/v1/organizations/{owner}/members/{member.user} | Invalidate run
[**update_organization**](OrganizationsV1Api.md#update_organization) | **PUT** /api/v1/organizations/{owner} | Get run
[**update_organization_member**](OrganizationsV1Api.md#update_organization_member) | **PUT** /api/v1/organizations/{owner}/members/{member.user} | Stop runs


# **create_organization**
> V1Organization create_organization(body)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
body = polyaxon_sdk.V1Organization() # V1Organization | 

try:
    # List runs
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_organization_member**
> V1OrganizationMember create_organization_member(owner, body)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body

try:
    # Delete runs
    api_response = api_instance.create_organization_member(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationsV1Api->create_organization_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization**
> delete_organization(owner)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace

try:
    # Patch run
    api_instance.delete_organization(owner)
except ApiException as e:
    print("Exception when calling OrganizationsV1Api->delete_organization: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_member**
> delete_organization_member(owner, member_user, member_role=member_role, member_created_at=member_created_at, member_updated_at=member_updated_at)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
member_user = 'member_user_example' # str | User
member_role = 'member_role_example' # str | Role. (optional)
member_created_at = '2013-10-20T19:20:30+01:00' # datetime | Optional time when the entityt was created. (optional)
member_updated_at = '2013-10-20T19:20:30+01:00' # datetime | Optional last time the entity was updated. (optional)

try:
    # Invalidate runs
    api_instance.delete_organization_member(owner, member_user, member_role=member_role, member_created_at=member_created_at, member_updated_at=member_updated_at)
except ApiException as e:
    print("Exception when calling OrganizationsV1Api->delete_organization_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **member_user** | **str**| User | 
 **member_role** | **str**| Role. | [optional] 
 **member_created_at** | **datetime**| Optional time when the entityt was created. | [optional] 
 **member_updated_at** | **datetime**| Optional last time the entity was updated. | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization**
> V1Organization get_organization(owner)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace

try:
    # Create new run
    api_response = api_instance.get_organization(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationsV1Api->get_organization: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_member**
> V1OrganizationMember get_organization_member(owner, member_user, member_role=member_role, member_created_at=member_created_at, member_updated_at=member_updated_at)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
member_user = 'member_user_example' # str | User
member_role = 'member_role_example' # str | Role. (optional)
member_created_at = '2013-10-20T19:20:30+01:00' # datetime | Optional time when the entityt was created. (optional)
member_updated_at = '2013-10-20T19:20:30+01:00' # datetime | Optional last time the entity was updated. (optional)

try:
    # Stop run
    api_response = api_instance.get_organization_member(owner, member_user, member_role=member_role, member_created_at=member_created_at, member_updated_at=member_updated_at)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationsV1Api->get_organization_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **member_user** | **str**| User | 
 **member_role** | **str**| Role. | [optional] 
 **member_created_at** | **datetime**| Optional time when the entityt was created. | [optional] 
 **member_updated_at** | **datetime**| Optional last time the entity was updated. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_organization_members**
> V1ListOrganizationMembersResponse list_organization_members(owner)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace

try:
    # Delete run
    api_response = api_instance.list_organization_members(owner)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganizationsV1Api->list_organization_members: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 

### Return type

[**V1ListOrganizationMembersResponse**](V1ListOrganizationMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_organization_names**
> V1ListOrganizationsResponse list_organization_names()

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))

try:
    # List bookmarked runs for user
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

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_organizations**
> V1ListOrganizationsResponse list_organizations()

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))

try:
    # List archived runs for user
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

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_organization**
> V1Organization patch_organization(owner, body)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Organization() # V1Organization | Organization body

try:
    # Update run
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_organization_member**
> V1OrganizationMember patch_organization_member(owner, member_user, body)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
member_user = 'member_user_example' # str | User
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body

try:
    # Invalidate run
    api_response = api_instance.patch_organization_member(owner, member_user, body)
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

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_organization**
> V1Organization update_organization(owner, body)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Organization() # V1Organization | Organization body

try:
    # Get run
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_organization_member**
> V1OrganizationMember update_organization_member(owner, member_user, body)

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
api_instance = polyaxon_sdk.OrganizationsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
member_user = 'member_user_example' # str | User
body = polyaxon_sdk.V1OrganizationMember() # V1OrganizationMember | Organization body

try:
    # Stop runs
    api_response = api_instance.update_organization_member(owner, member_user, body)
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

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

