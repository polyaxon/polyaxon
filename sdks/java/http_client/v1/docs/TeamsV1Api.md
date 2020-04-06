# TeamsV1Api

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
    V1Team result = apiInstance.teamsV1CreateTeam(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1CreateTeam");
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

<a name="teamsV1CreateTeamMember"></a>
# **teamsV1CreateTeamMember**
> V1TeamMember teamsV1CreateTeamMember(owner, team, body)

Create organization member

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
    V1TeamMember result = apiInstance.teamsV1CreateTeamMember(owner, team, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1CreateTeamMember");
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

<a name="teamsV1DeleteTeam"></a>
# **teamsV1DeleteTeam**
> teamsV1DeleteTeam(owner, team)

Delete organization

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
    apiInstance.teamsV1DeleteTeam(owner, team);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1DeleteTeam");
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

<a name="teamsV1DeleteTeamMember"></a>
# **teamsV1DeleteTeamMember**
> teamsV1DeleteTeamMember(owner, team, user)

Delete organization member details

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
    apiInstance.teamsV1DeleteTeamMember(owner, team, user);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1DeleteTeamMember");
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
    V1Team result = apiInstance.teamsV1GetTeam(owner, team);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1GetTeam");
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

<a name="teamsV1GetTeamMember"></a>
# **teamsV1GetTeamMember**
> V1TeamMember teamsV1GetTeamMember(owner, team, user)

Get organization member details

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
    V1TeamMember result = apiInstance.teamsV1GetTeamMember(owner, team, user);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1GetTeamMember");
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

<a name="teamsV1ListTeamMembers"></a>
# **teamsV1ListTeamMembers**
> V1ListTeamMembersResponse teamsV1ListTeamMembers(owner, team, offset, limit, sort, query)

Get organization members

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
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListTeamMembersResponse result = apiInstance.teamsV1ListTeamMembers(owner, team, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1ListTeamMembers");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **team** | **String**| Team under namesapce |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
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
> V1ListTeamsResponse teamsV1ListTeamNames(owner, offset, limit, sort, query)

List organizations names

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
    V1ListTeamsResponse result = apiInstance.teamsV1ListTeamNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1ListTeamNames");
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

<a name="teamsV1ListTeams"></a>
# **teamsV1ListTeams**
> V1ListTeamsResponse teamsV1ListTeams(owner, offset, limit, sort, query)

List organizations

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
    V1ListTeamsResponse result = apiInstance.teamsV1ListTeams(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1ListTeams");
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

<a name="teamsV1PatchTeam"></a>
# **teamsV1PatchTeam**
> V1Team teamsV1PatchTeam(owner, teamName, body)

Patch organization

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
    V1Team result = apiInstance.teamsV1PatchTeam(owner, teamName, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1PatchTeam");
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

<a name="teamsV1PatchTeamMember"></a>
# **teamsV1PatchTeamMember**
> V1TeamMember teamsV1PatchTeamMember(owner, team, memberUser, body)

Patch organization member

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
    V1TeamMember result = apiInstance.teamsV1PatchTeamMember(owner, team, memberUser, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1PatchTeamMember");
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

<a name="teamsV1UpdateTeam"></a>
# **teamsV1UpdateTeam**
> V1Team teamsV1UpdateTeam(owner, teamName, body)

Update organization

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
    V1Team result = apiInstance.teamsV1UpdateTeam(owner, teamName, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1UpdateTeam");
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

<a name="teamsV1UpdateTeamMember"></a>
# **teamsV1UpdateTeamMember**
> V1TeamMember teamsV1UpdateTeamMember(owner, team, memberUser, body)

Update organization member

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
    V1TeamMember result = apiInstance.teamsV1UpdateTeamMember(owner, team, memberUser, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling TeamsV1Api#teamsV1UpdateTeamMember");
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

