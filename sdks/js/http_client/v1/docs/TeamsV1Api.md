# PolyaxonSdk.TeamsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**teamsV1CreateTeam**](TeamsV1Api.md#teamsV1CreateTeam) | **POST** /api/v1/orgs/{owner}/teams | Create organization
[**teamsV1CreateTeamMember**](TeamsV1Api.md#teamsV1CreateTeamMember) | **POST** /api/v1/orgs/{owner}/teams/{team}/members | Create organization member
[**teamsV1DeleteTeam**](TeamsV1Api.md#teamsV1DeleteTeam) | **DELETE** /api/v1/orgs/{owner}/teams/{team} | Delete organization
[**teamsV1DeleteTeamMember**](TeamsV1Api.md#teamsV1DeleteTeamMember) | **DELETE** /api/v1/orgs/{owner}/teams/{team}/members/{user} | Delete organization member details
[**teamsV1GetTeam**](TeamsV1Api.md#teamsV1GetTeam) | **GET** /api/v1/orgs/{owner}/teams/{team} | Get organization
[**teamsV1GetTeamMember**](TeamsV1Api.md#teamsV1GetTeamMember) | **GET** /api/v1/orgs/{owner}/teams/{team}/members/{user} | Get organization member details
[**teamsV1ListTeamMembers**](TeamsV1Api.md#teamsV1ListTeamMembers) | **GET** /api/v1/orgs/{owner}/teams/{team}/members | Get organization members
[**teamsV1ListTeamNames**](TeamsV1Api.md#teamsV1ListTeamNames) | **GET** /api/v1/orgs/{owner}/teams/names | List organizations names
[**teamsV1ListTeams**](TeamsV1Api.md#teamsV1ListTeams) | **GET** /api/v1/orgs/{owner}/teams | List organizations
[**teamsV1PatchTeam**](TeamsV1Api.md#teamsV1PatchTeam) | **PATCH** /api/v1/orgs/{owner}/teams/{team.name} | Patch organization
[**teamsV1PatchTeamMember**](TeamsV1Api.md#teamsV1PatchTeamMember) | **PATCH** /api/v1/orgs/{owner}/teams/{team}/members/{member.user} | Patch organization member
[**teamsV1UpdateTeam**](TeamsV1Api.md#teamsV1UpdateTeam) | **PUT** /api/v1/orgs/{owner}/teams/{team.name} | Update organization
[**teamsV1UpdateTeamMember**](TeamsV1Api.md#teamsV1UpdateTeamMember) | **PUT** /api/v1/orgs/{owner}/teams/{team}/members/{member.user} | Update organization member


<a name="teamsV1CreateTeam"></a>
# **teamsV1CreateTeam**
> V1Team teamsV1CreateTeam(owner, body)

Create organization

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1Team(); // V1Team | Team body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1CreateTeam(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Team**](V1Team.md)| Team body | 

### Return type

[**V1Team**](V1Team.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1CreateTeamMember"></a>
# **teamsV1CreateTeamMember**
> V1TeamMember teamsV1CreateTeamMember(owner, team, body)

Create organization member

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team = "team_example"; // String | Team

var body = new PolyaxonSdk.V1TeamMember(); // V1TeamMember | Team body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1CreateTeamMember(owner, team, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team** | **String**| Team | 
 **body** | [**V1TeamMember**](V1TeamMember.md)| Team body | 

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1DeleteTeam"></a>
# **teamsV1DeleteTeam**
> teamsV1DeleteTeam(owner, team)

Delete organization

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team = "team_example"; // String | Team under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.teamsV1DeleteTeam(owner, team, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team** | **String**| Team under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1DeleteTeamMember"></a>
# **teamsV1DeleteTeamMember**
> teamsV1DeleteTeamMember(owner, team, user)

Delete organization member details

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team = "team_example"; // String | Team under namesapce

var user = "user_example"; // String | Member under team


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.teamsV1DeleteTeamMember(owner, team, user, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team** | **String**| Team under namesapce | 
 **user** | **String**| Member under team | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1GetTeam"></a>
# **teamsV1GetTeam**
> V1Team teamsV1GetTeam(owner, team)

Get organization

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team = "team_example"; // String | Team under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1GetTeam(owner, team, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team** | **String**| Team under namesapce | 

### Return type

[**V1Team**](V1Team.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1GetTeamMember"></a>
# **teamsV1GetTeamMember**
> V1TeamMember teamsV1GetTeamMember(owner, team, user)

Get organization member details

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team = "team_example"; // String | Team under namesapce

var user = "user_example"; // String | Member under team


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1GetTeamMember(owner, team, user, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team** | **String**| Team under namesapce | 
 **user** | **String**| Member under team | 

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1ListTeamMembers"></a>
# **teamsV1ListTeamMembers**
> V1ListTeamMembersResponse teamsV1ListTeamMembers(owner, team, opts)

Get organization members

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team = "team_example"; // String | Team under namesapce

var opts = { 
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1ListTeamMembers(owner, team, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team** | **String**| Team under namesapce | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListTeamMembersResponse**](V1ListTeamMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1ListTeamNames"></a>
# **teamsV1ListTeamNames**
> V1ListTeamsResponse teamsV1ListTeamNames(owner, opts)

List organizations names

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var opts = { 
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1ListTeamNames(owner, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListTeamsResponse**](V1ListTeamsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1ListTeams"></a>
# **teamsV1ListTeams**
> V1ListTeamsResponse teamsV1ListTeams(owner, opts)

List organizations

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var opts = { 
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1ListTeams(owner, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListTeamsResponse**](V1ListTeamsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1PatchTeam"></a>
# **teamsV1PatchTeam**
> V1Team teamsV1PatchTeam(owner, team_name, body)

Patch organization

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team_name = "team_name_example"; // String | Name

var body = new PolyaxonSdk.V1Team(); // V1Team | Team body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1PatchTeam(owner, team_name, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team_name** | **String**| Name | 
 **body** | [**V1Team**](V1Team.md)| Team body | 

### Return type

[**V1Team**](V1Team.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1PatchTeamMember"></a>
# **teamsV1PatchTeamMember**
> V1TeamMember teamsV1PatchTeamMember(owner, team, member_user, body)

Patch organization member

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team = "team_example"; // String | Team

var member_user = "member_user_example"; // String | User

var body = new PolyaxonSdk.V1TeamMember(); // V1TeamMember | Team body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1PatchTeamMember(owner, team, member_user, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team** | **String**| Team | 
 **member_user** | **String**| User | 
 **body** | [**V1TeamMember**](V1TeamMember.md)| Team body | 

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1UpdateTeam"></a>
# **teamsV1UpdateTeam**
> V1Team teamsV1UpdateTeam(owner, team_name, body)

Update organization

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team_name = "team_name_example"; // String | Name

var body = new PolyaxonSdk.V1Team(); // V1Team | Team body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1UpdateTeam(owner, team_name, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team_name** | **String**| Name | 
 **body** | [**V1Team**](V1Team.md)| Team body | 

### Return type

[**V1Team**](V1Team.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="teamsV1UpdateTeamMember"></a>
# **teamsV1UpdateTeamMember**
> V1TeamMember teamsV1UpdateTeamMember(owner, team, member_user, body)

Update organization member

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.TeamsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var team = "team_example"; // String | Team

var member_user = "member_user_example"; // String | User

var body = new PolyaxonSdk.V1TeamMember(); // V1TeamMember | Team body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.teamsV1UpdateTeamMember(owner, team, member_user, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **team** | **String**| Team | 
 **member_user** | **String**| User | 
 **body** | [**V1TeamMember**](V1TeamMember.md)| Team body | 

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

