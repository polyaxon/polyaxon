# TeamsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createTeam**](TeamsV1Api.md#createTeam) | **POST** /api/v1/{owner}/teams | List runs
[**createTeamMember**](TeamsV1Api.md#createTeamMember) | **POST** /api/v1/{owner}/teams/{team}/members | Delete runs
[**deleteTeam**](TeamsV1Api.md#deleteTeam) | **DELETE** /api/v1/{owner}/teams/{team} | Patch run
[**deleteTeamMember**](TeamsV1Api.md#deleteTeamMember) | **DELETE** /api/v1/{owner}/teams/{team}/members/{member.user} | Invalidate runs
[**getTeam**](TeamsV1Api.md#getTeam) | **GET** /api/v1/{owner}/teams/{team} | Create new run
[**getTeamMember**](TeamsV1Api.md#getTeamMember) | **GET** /api/v1/{owner}/teams/{team}/members/{user} | Stop run
[**listTeamMembers**](TeamsV1Api.md#listTeamMembers) | **GET** /api/v1/{owner}/teams/{team}/members | Delete run
[**listTeamNames**](TeamsV1Api.md#listTeamNames) | **GET** /api/v1/{owner}/teams/names | List bookmarked runs for user
[**listTeams**](TeamsV1Api.md#listTeams) | **GET** /api/v1/{owner}/teams | List archived runs for user
[**patchTeam**](TeamsV1Api.md#patchTeam) | **PATCH** /api/v1/{owner}/teams/{team.name} | Update run
[**patchTeamMember**](TeamsV1Api.md#patchTeamMember) | **PATCH** /api/v1/{owner}/teams/{team}/members/{member.user} | Invalidate run
[**updateTeam**](TeamsV1Api.md#updateTeam) | **PUT** /api/v1/{owner}/teams/{team.name} | Get run
[**updateTeamMember**](TeamsV1Api.md#updateTeamMember) | **PUT** /api/v1/{owner}/teams/{team}/members/{member.user} | Stop runs


<a name="createTeam"></a>
# **createTeam**
> V1Team createTeam(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1Team body = new V1Team(); // V1Team | Team body
try {
    V1Team result = apiInstance.createTeam(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#createTeam");
    e.printStackTrace();
}
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

Delete runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String team = "team_example"; // String | Team
V1TeamMember body = new V1TeamMember(); // V1TeamMember | Team body
try {
    V1TeamMember result = apiInstance.createTeamMember(owner, team, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#createTeamMember");
    e.printStackTrace();
}
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

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String team = "team_example"; // String | Team under namesapce
try {
    apiInstance.deleteTeam(owner, team);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#deleteTeam");
    e.printStackTrace();
}
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
> deleteTeamMember(owner, team, memberUser, memberRole, memberOrgRole, memberCreatedAt, memberUpdatedAt)

Invalidate runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String team = "team_example"; // String | Team
String memberUser = "memberUser_example"; // String | User
String memberRole = "memberRole_example"; // String | Role.
String memberOrgRole = "memberOrgRole_example"; // String | Organization Role.
OffsetDateTime memberCreatedAt = OffsetDateTime.now(); // OffsetDateTime | Optional time when the entityt was created.
OffsetDateTime memberUpdatedAt = OffsetDateTime.now(); // OffsetDateTime | Optional last time the entity was updated.
try {
    apiInstance.deleteTeamMember(owner, team, memberUser, memberRole, memberOrgRole, memberCreatedAt, memberUpdatedAt);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#deleteTeamMember");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **team** | **String**| Team |
 **memberUser** | **String**| User |
 **memberRole** | **String**| Role. | [optional]
 **memberOrgRole** | **String**| Organization Role. | [optional]
 **memberCreatedAt** | **OffsetDateTime**| Optional time when the entityt was created. | [optional]
 **memberUpdatedAt** | **OffsetDateTime**| Optional last time the entity was updated. | [optional]

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

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String team = "team_example"; // String | Team under namesapce
try {
    V1Team result = apiInstance.getTeam(owner, team);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#getTeam");
    e.printStackTrace();
}
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

Stop run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String team = "team_example"; // String | Team under namesapce
String user = "user_example"; // String | Member under team
try {
    V1TeamMember result = apiInstance.getTeamMember(owner, team, user);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#getTeamMember");
    e.printStackTrace();
}
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
> V1ListTeamMembersResponse listTeamMembers(owner, team)

Delete run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String team = "team_example"; // String | Team under namesapce
try {
    V1ListTeamMembersResponse result = apiInstance.listTeamMembers(owner, team);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#listTeamMembers");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **team** | **String**| Team under namesapce |

### Return type

[**V1ListTeamMembersResponse**](V1ListTeamMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listTeamNames"></a>
# **listTeamNames**
> V1ListTeamsResponse listTeamNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListTeamsResponse result = apiInstance.listTeamNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#listTeamNames");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
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
> V1ListTeamsResponse listTeams(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListTeamsResponse result = apiInstance.listTeams(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#listTeams");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
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
> V1Team patchTeam(owner, teamName, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String teamName = "teamName_example"; // String | Name
V1Team body = new V1Team(); // V1Team | Team body
try {
    V1Team result = apiInstance.patchTeam(owner, teamName, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#patchTeam");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **teamName** | **String**| Name |
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
> V1TeamMember patchTeamMember(owner, team, memberUser, body)

Invalidate run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String team = "team_example"; // String | Team
String memberUser = "memberUser_example"; // String | User
V1TeamMember body = new V1TeamMember(); // V1TeamMember | Team body
try {
    V1TeamMember result = apiInstance.patchTeamMember(owner, team, memberUser, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#patchTeamMember");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **team** | **String**| Team |
 **memberUser** | **String**| User |
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
> V1Team updateTeam(owner, teamName, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String teamName = "teamName_example"; // String | Name
V1Team body = new V1Team(); // V1Team | Team body
try {
    V1Team result = apiInstance.updateTeam(owner, teamName, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#updateTeam");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **teamName** | **String**| Name |
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
> V1TeamMember updateTeamMember(owner, team, memberUser, body)

Stop runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.TeamsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

TeamsV1Api apiInstance = new TeamsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String team = "team_example"; // String | Team
String memberUser = "memberUser_example"; // String | User
V1TeamMember body = new V1TeamMember(); // V1TeamMember | Team body
try {
    V1TeamMember result = apiInstance.updateTeamMember(owner, team, memberUser, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#updateTeamMember");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **team** | **String**| Team |
 **memberUser** | **String**| User |
 **body** | [**V1TeamMember**](V1TeamMember.md)| Team body |

### Return type

[**V1TeamMember**](V1TeamMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

