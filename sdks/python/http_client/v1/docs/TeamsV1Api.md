# polyaxon_sdk.TeamsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_team**](TeamsV1Api.md#create_team) | **POST** /api/v1/{owner}/teams | List runs
[**create_team_member**](TeamsV1Api.md#create_team_member) | **POST** /api/v1/{owner}/teams/{team}/members | Delete runs
[**delete_team**](TeamsV1Api.md#delete_team) | **DELETE** /api/v1/{owner}/teams/{team} | Patch run
[**delete_team_member**](TeamsV1Api.md#delete_team_member) | **DELETE** /api/v1/{owner}/teams/{team}/members/{member.user} | Invalidate runs
[**get_team**](TeamsV1Api.md#get_team) | **GET** /api/v1/{owner}/teams/{team} | Create new run
[**get_team_member**](TeamsV1Api.md#get_team_member) | **GET** /api/v1/{owner}/teams/{team}/members/{user} | Stop run
[**list_team_members**](TeamsV1Api.md#list_team_members) | **GET** /api/v1/{owner}/teams/{team}/members | Delete run
[**list_team_names**](TeamsV1Api.md#list_team_names) | **GET** /api/v1/{owner}/teams/names | List bookmarked runs for user
[**list_teams**](TeamsV1Api.md#list_teams) | **GET** /api/v1/{owner}/teams | List archived runs for user
[**patch_team**](TeamsV1Api.md#patch_team) | **PATCH** /api/v1/{owner}/teams/{team.name} | Update run
[**patch_team_member**](TeamsV1Api.md#patch_team_member) | **PATCH** /api/v1/{owner}/teams/{team}/members/{member.user} | Invalidate run
[**update_team**](TeamsV1Api.md#update_team) | **PUT** /api/v1/{owner}/teams/{team.name} | Get run
[**update_team_member**](TeamsV1Api.md#update_team_member) | **PUT** /api/v1/{owner}/teams/{team}/members/{member.user} | Stop runs


# **create_team**
> V1Team create_team(owner, body)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
body = polyaxon_sdk.V1Team() # V1Team | Team body

try:
    # List runs
    api_response = api_instance.create_team(owner, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->create_team: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **body** | [**V1Team**](V1Team.md)| Team body | 

### Return type

[**V1Team**](V1Team.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_team_member**
> V1TeamMember create_team_member(owner, team, body)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team = 'team_example' # str | Team
body = polyaxon_sdk.V1TeamMember() # V1TeamMember | Team body

try:
    # Delete runs
    api_response = api_instance.create_team_member(owner, team, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->create_team_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team** | **str**| Team | 
 **body** | [**V1TeamMember**](V1TeamMember.md)| Team body | 

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_team**
> delete_team(owner, team)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team = 'team_example' # str | Team under namesapce

try:
    # Patch run
    api_instance.delete_team(owner, team)
except ApiException as e:
    print("Exception when calling TeamsV1Api->delete_team: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team** | **str**| Team under namesapce | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_team_member**
> delete_team_member(owner, team, member_user, member_role=member_role, member_org_role=member_org_role, member_created_at=member_created_at, member_updated_at=member_updated_at)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team = 'team_example' # str | Team
member_user = 'member_user_example' # str | User
member_role = 'member_role_example' # str | Role. (optional)
member_org_role = 'member_org_role_example' # str | Organization Role. (optional)
member_created_at = '2013-10-20T19:20:30+01:00' # datetime | Optional time when the entityt was created. (optional)
member_updated_at = '2013-10-20T19:20:30+01:00' # datetime | Optional last time the entity was updated. (optional)

try:
    # Invalidate runs
    api_instance.delete_team_member(owner, team, member_user, member_role=member_role, member_org_role=member_org_role, member_created_at=member_created_at, member_updated_at=member_updated_at)
except ApiException as e:
    print("Exception when calling TeamsV1Api->delete_team_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team** | **str**| Team | 
 **member_user** | **str**| User | 
 **member_role** | **str**| Role. | [optional] 
 **member_org_role** | **str**| Organization Role. | [optional] 
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

# **get_team**
> V1Team get_team(owner, team)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team = 'team_example' # str | Team under namesapce

try:
    # Create new run
    api_response = api_instance.get_team(owner, team)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->get_team: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team** | **str**| Team under namesapce | 

### Return type

[**V1Team**](V1Team.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_team_member**
> V1TeamMember get_team_member(owner, team, user)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team = 'team_example' # str | Team under namesapce
user = 'user_example' # str | Member under team

try:
    # Stop run
    api_response = api_instance.get_team_member(owner, team, user)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->get_team_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team** | **str**| Team under namesapce | 
 **user** | **str**| Member under team | 

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_team_members**
> V1ListTeamMembersResponse list_team_members(owner, team)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team = 'team_example' # str | Team under namesapce

try:
    # Delete run
    api_response = api_instance.list_team_members(owner, team)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->list_team_members: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team** | **str**| Team under namesapce | 

### Return type

[**V1ListTeamMembersResponse**](V1ListTeamMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_team_names**
> V1ListTeamsResponse list_team_names(owner, offset=offset, limit=limit, sort=sort, query=query)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List bookmarked runs for user
    api_response = api_instance.list_team_names(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->list_team_names: %s\n" % e)
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

[**V1ListTeamsResponse**](V1ListTeamsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_teams**
> V1ListTeamsResponse list_teams(owner, offset=offset, limit=limit, sort=sort, query=query)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
offset = 56 # int | Pagination offset. (optional)
limit = 56 # int | Limit size. (optional)
sort = 'sort_example' # str | Sort to order the search. (optional)
query = 'query_example' # str | Query filter the search search. (optional)

try:
    # List archived runs for user
    api_response = api_instance.list_teams(owner, offset=offset, limit=limit, sort=sort, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->list_teams: %s\n" % e)
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

[**V1ListTeamsResponse**](V1ListTeamsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_team**
> V1Team patch_team(owner, team_name, body)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team_name = 'team_name_example' # str | Name
body = polyaxon_sdk.V1Team() # V1Team | Team body

try:
    # Update run
    api_response = api_instance.patch_team(owner, team_name, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->patch_team: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team_name** | **str**| Name | 
 **body** | [**V1Team**](V1Team.md)| Team body | 

### Return type

[**V1Team**](V1Team.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_team_member**
> V1TeamMember patch_team_member(owner, team, member_user, body)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team = 'team_example' # str | Team
member_user = 'member_user_example' # str | User
body = polyaxon_sdk.V1TeamMember() # V1TeamMember | Team body

try:
    # Invalidate run
    api_response = api_instance.patch_team_member(owner, team, member_user, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->patch_team_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team** | **str**| Team | 
 **member_user** | **str**| User | 
 **body** | [**V1TeamMember**](V1TeamMember.md)| Team body | 

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_team**
> V1Team update_team(owner, team_name, body)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team_name = 'team_name_example' # str | Name
body = polyaxon_sdk.V1Team() # V1Team | Team body

try:
    # Get run
    api_response = api_instance.update_team(owner, team_name, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->update_team: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team_name** | **str**| Name | 
 **body** | [**V1Team**](V1Team.md)| Team body | 

### Return type

[**V1Team**](V1Team.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_team_member**
> V1TeamMember update_team_member(owner, team, member_user, body)

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
api_instance = polyaxon_sdk.TeamsV1Api(polyaxon_sdk.ApiClient(configuration))
owner = 'owner_example' # str | Owner of the namespace
team = 'team_example' # str | Team
member_user = 'member_user_example' # str | User
body = polyaxon_sdk.V1TeamMember() # V1TeamMember | Team body

try:
    # Stop runs
    api_response = api_instance.update_team_member(owner, team, member_user, body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsV1Api->update_team_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **str**| Owner of the namespace | 
 **team** | **str**| Team | 
 **member_user** | **str**| User | 
 **body** | [**V1TeamMember**](V1TeamMember.md)| Team body | 

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

