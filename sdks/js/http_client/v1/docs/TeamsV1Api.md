# PolyaxonSdk.TeamsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createTeam**](TeamsV1Api.md#createTeam) | **POST** /api/v1/orgs/{owner}/teams | Create organization
[**createTeamMember**](TeamsV1Api.md#createTeamMember) | **POST** /api/v1/orgs/{owner}/teams/{team}/members | Create organization member
[**deleteTeam**](TeamsV1Api.md#deleteTeam) | **DELETE** /api/v1/orgs/{owner}/teams/{team} | Delete organization
[**deleteTeamMember**](TeamsV1Api.md#deleteTeamMember) | **DELETE** /api/v1/orgs/{owner}/teams/{team}/members/{user} | Delete organization member details
[**getTeam**](TeamsV1Api.md#getTeam) | **GET** /api/v1/orgs/{owner}/teams/{team} | Get organization
[**getTeamMember**](TeamsV1Api.md#getTeamMember) | **GET** /api/v1/orgs/{owner}/teams/{team}/members/{user} | Get organization member details
[**listTeamMembers**](TeamsV1Api.md#listTeamMembers) | **GET** /api/v1/orgs/{owner}/teams/{team}/members | Get organization members
[**listTeamNames**](TeamsV1Api.md#listTeamNames) | **GET** /api/v1/orgs/{owner}/teams/names | List organizations names
[**listTeams**](TeamsV1Api.md#listTeams) | **GET** /api/v1/orgs/{owner}/teams | List organizations
[**patchTeam**](TeamsV1Api.md#patchTeam) | **PATCH** /api/v1/orgs/{owner}/teams/{team.name} | Patch organization
[**patchTeamMember**](TeamsV1Api.md#patchTeamMember) | **PATCH** /api/v1/orgs/{owner}/teams/{team}/members/{member.user} | Patch organization member
[**updateTeam**](TeamsV1Api.md#updateTeam) | **PUT** /api/v1/orgs/{owner}/teams/{team.name} | Update organization
[**updateTeamMember**](TeamsV1Api.md#updateTeamMember) | **PUT** /api/v1/orgs/{owner}/teams/{team}/members/{member.user} | Update organization member


<a name="createTeam"></a>
# **createTeam**
> V1Team createTeam(owner, body)

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
apiInstance.createTeam(owner, body, callback);
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

<a name="createTeamMember"></a>
# **createTeamMember**
> V1TeamMember createTeamMember(owner, team, body)

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
apiInstance.createTeamMember(owner, team, body, callback);
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

<a name="deleteTeam"></a>
# **deleteTeam**
> deleteTeam(owner, team)

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
apiInstance.deleteTeam(owner, team, callback);
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

<a name="deleteTeamMember"></a>
# **deleteTeamMember**
> deleteTeamMember(owner, team, user)

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
apiInstance.deleteTeamMember(owner, team, user, callback);
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

<a name="getTeam"></a>
# **getTeam**
> V1Team getTeam(owner, team)

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
apiInstance.getTeam(owner, team, callback);
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

<a name="getTeamMember"></a>
# **getTeamMember**
> V1TeamMember getTeamMember(owner, team, user)

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
apiInstance.getTeamMember(owner, team, user, callback);
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

<a name="listTeamMembers"></a>
# **listTeamMembers**
> V1ListTeamMembersResponse listTeamMembers(owner, team, opts)

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
apiInstance.listTeamMembers(owner, team, opts, callback);
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

<a name="listTeamNames"></a>
# **listTeamNames**
> V1ListTeamsResponse listTeamNames(owner, opts)

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
apiInstance.listTeamNames(owner, opts, callback);
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

<a name="listTeams"></a>
# **listTeams**
> V1ListTeamsResponse listTeams(owner, opts)

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
apiInstance.listTeams(owner, opts, callback);
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

<a name="patchTeam"></a>
# **patchTeam**
> V1Team patchTeam(owner, team_name, body)

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
apiInstance.patchTeam(owner, team_name, body, callback);
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

<a name="patchTeamMember"></a>
# **patchTeamMember**
> V1TeamMember patchTeamMember(owner, team, member_user, body)

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
apiInstance.patchTeamMember(owner, team, member_user, body, callback);
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

<a name="updateTeam"></a>
# **updateTeam**
> V1Team updateTeam(owner, team_name, body)

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
apiInstance.updateTeam(owner, team_name, body, callback);
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

<a name="updateTeamMember"></a>
# **updateTeamMember**
> V1TeamMember updateTeamMember(owner, team, member_user, body)

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
apiInstance.updateTeamMember(owner, team, member_user, body, callback);
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

