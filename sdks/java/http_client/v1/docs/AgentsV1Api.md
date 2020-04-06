# AgentsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**agentsV1CreateAgent**](AgentsV1Api.md#agentsV1CreateAgent) | **POST** /api/v1/orgs/{owner}/agents | Create run profile
[**agentsV1CreateAgentStatus**](AgentsV1Api.md#agentsV1CreateAgentStatus) | **POST** /api/v1/orgs/{owner}/agents/{uuid}/statuses | 
[**agentsV1DeleteAgent**](AgentsV1Api.md#agentsV1DeleteAgent) | **DELETE** /api/v1/orgs/{owner}/agents/{uuid} | Delete run profile
[**agentsV1GetAgent**](AgentsV1Api.md#agentsV1GetAgent) | **GET** /api/v1/orgs/{owner}/agents/{uuid} | Get run profile
[**agentsV1GetAgentState**](AgentsV1Api.md#agentsV1GetAgentState) | **GET** /api/v1/orgs/{owner}/agents/{uuid}/state | 
[**agentsV1GetAgentStatuses**](AgentsV1Api.md#agentsV1GetAgentStatuses) | **GET** /api/v1/orgs/{owner}/agents/{uuid}/statuses | 
[**agentsV1ListAgentNames**](AgentsV1Api.md#agentsV1ListAgentNames) | **GET** /api/v1/orgs/{owner}/agents/names | List run profiles names
[**agentsV1ListAgents**](AgentsV1Api.md#agentsV1ListAgents) | **GET** /api/v1/orgs/{owner}/agents | List run profiles
[**agentsV1PatchAgent**](AgentsV1Api.md#agentsV1PatchAgent) | **PATCH** /api/v1/orgs/{owner}/agents/{agent.uuid} | Patch run profile
[**agentsV1SyncAgent**](AgentsV1Api.md#agentsV1SyncAgent) | **PATCH** /api/v1/orgs/{owner}/agents/{agent.uuid}/sync | 
[**agentsV1UpdateAgent**](AgentsV1Api.md#agentsV1UpdateAgent) | **PUT** /api/v1/orgs/{owner}/agents/{agent.uuid} | Update run profile


<a name="agentsV1CreateAgent"></a>
# **agentsV1CreateAgent**
> V1Agent agentsV1CreateAgent(owner, body)

Create run profile

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1Agent body = new V1Agent(); // V1Agent | Agent body
try {
    V1Agent result = apiInstance.agentsV1CreateAgent(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1CreateAgent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1Agent**](V1Agent.md)| Agent body |

### Return type

[**V1Agent**](V1Agent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1CreateAgentStatus"></a>
# **agentsV1CreateAgentStatus**
> V1Status agentsV1CreateAgentStatus(owner, uuid, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
V1AgentStatusBodyRequest body = new V1AgentStatusBodyRequest(); // V1AgentStatusBodyRequest | 
try {
    V1Status result = apiInstance.agentsV1CreateAgentStatus(owner, uuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1CreateAgentStatus");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |
 **body** | [**V1AgentStatusBodyRequest**](V1AgentStatusBodyRequest.md)|  |

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1DeleteAgent"></a>
# **agentsV1DeleteAgent**
> agentsV1DeleteAgent(owner, uuid)

Delete run profile

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.agentsV1DeleteAgent(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1DeleteAgent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1GetAgent"></a>
# **agentsV1GetAgent**
> V1Agent agentsV1GetAgent(owner, uuid)

Get run profile

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Agent result = apiInstance.agentsV1GetAgent(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1GetAgent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1Agent**](V1Agent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1GetAgentState"></a>
# **agentsV1GetAgentState**
> V1AgentStateResponse agentsV1GetAgentState(owner, uuid)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1AgentStateResponse result = apiInstance.agentsV1GetAgentState(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1GetAgentState");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1AgentStateResponse**](V1AgentStateResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1GetAgentStatuses"></a>
# **agentsV1GetAgentStatuses**
> V1Status agentsV1GetAgentStatuses(owner, uuid)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Status result = apiInstance.agentsV1GetAgentStatuses(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1GetAgentStatuses");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1ListAgentNames"></a>
# **agentsV1ListAgentNames**
> V1ListAgentsResponse agentsV1ListAgentNames(owner, offset, limit, sort, query)

List run profiles names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListAgentsResponse result = apiInstance.agentsV1ListAgentNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1ListAgentNames");
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

[**V1ListAgentsResponse**](V1ListAgentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1ListAgents"></a>
# **agentsV1ListAgents**
> V1ListAgentsResponse agentsV1ListAgents(owner, offset, limit, sort, query)

List run profiles

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListAgentsResponse result = apiInstance.agentsV1ListAgents(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1ListAgents");
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

[**V1ListAgentsResponse**](V1ListAgentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1PatchAgent"></a>
# **agentsV1PatchAgent**
> V1Agent agentsV1PatchAgent(owner, agentUuid, body)

Patch run profile

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String agentUuid = "agentUuid_example"; // String | UUID
V1Agent body = new V1Agent(); // V1Agent | Agent body
try {
    V1Agent result = apiInstance.agentsV1PatchAgent(owner, agentUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1PatchAgent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **agentUuid** | **String**| UUID |
 **body** | [**V1Agent**](V1Agent.md)| Agent body |

### Return type

[**V1Agent**](V1Agent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1SyncAgent"></a>
# **agentsV1SyncAgent**
> agentsV1SyncAgent(owner, agentUuid, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String agentUuid = "agentUuid_example"; // String | UUID
V1Agent body = new V1Agent(); // V1Agent | Agent body
try {
    apiInstance.agentsV1SyncAgent(owner, agentUuid, body);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1SyncAgent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **agentUuid** | **String**| UUID |
 **body** | [**V1Agent**](V1Agent.md)| Agent body |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="agentsV1UpdateAgent"></a>
# **agentsV1UpdateAgent**
> V1Agent agentsV1UpdateAgent(owner, agentUuid, body)

Update run profile

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AgentsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AgentsV1Api apiInstance = new AgentsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String agentUuid = "agentUuid_example"; // String | UUID
V1Agent body = new V1Agent(); // V1Agent | Agent body
try {
    V1Agent result = apiInstance.agentsV1UpdateAgent(owner, agentUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#agentsV1UpdateAgent");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **agentUuid** | **String**| UUID |
 **body** | [**V1Agent**](V1Agent.md)| Agent body |

### Return type

[**V1Agent**](V1Agent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

