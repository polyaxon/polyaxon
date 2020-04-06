# AgentsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createAgent**](AgentsV1Api.md#createAgent) | **POST** /api/v1/orgs/{owner}/agents | Create run profile
[**createAgentStatus**](AgentsV1Api.md#createAgentStatus) | **POST** /api/v1/orgs/{owner}/agents/{uuid}/statuses | 
[**deleteAgent**](AgentsV1Api.md#deleteAgent) | **DELETE** /api/v1/orgs/{owner}/agents/{uuid} | Delete run profile
[**getAgent**](AgentsV1Api.md#getAgent) | **GET** /api/v1/orgs/{owner}/agents/{uuid} | Get run profile
[**getAgentState**](AgentsV1Api.md#getAgentState) | **GET** /api/v1/orgs/{owner}/agents/{uuid}/state | 
[**getAgentStatuses**](AgentsV1Api.md#getAgentStatuses) | **GET** /api/v1/orgs/{owner}/agents/{uuid}/statuses | 
[**listAgentNames**](AgentsV1Api.md#listAgentNames) | **GET** /api/v1/orgs/{owner}/agents/names | List run profiles names
[**listAgents**](AgentsV1Api.md#listAgents) | **GET** /api/v1/orgs/{owner}/agents | List run profiles
[**patchAgent**](AgentsV1Api.md#patchAgent) | **PATCH** /api/v1/orgs/{owner}/agents/{agent.uuid} | Patch run profile
[**syncAgent**](AgentsV1Api.md#syncAgent) | **PATCH** /api/v1/orgs/{owner}/agents/{agent.uuid}/sync | 
[**updateAgent**](AgentsV1Api.md#updateAgent) | **PUT** /api/v1/orgs/{owner}/agents/{agent.uuid} | Update run profile


<a name="createAgent"></a>
# **createAgent**
> V1Agent createAgent(owner, body)

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
    V1Agent result = apiInstance.createAgent(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#createAgent");
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

<a name="createAgentStatus"></a>
# **createAgentStatus**
> V1Status createAgentStatus(owner, uuid, body)



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
    V1Status result = apiInstance.createAgentStatus(owner, uuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#createAgentStatus");
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

<a name="deleteAgent"></a>
# **deleteAgent**
> deleteAgent(owner, uuid)

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
    apiInstance.deleteAgent(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#deleteAgent");
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

<a name="getAgent"></a>
# **getAgent**
> V1Agent getAgent(owner, uuid)

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
    V1Agent result = apiInstance.getAgent(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#getAgent");
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

<a name="getAgentState"></a>
# **getAgentState**
> V1AgentStateResponse getAgentState(owner, uuid)



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
    V1AgentStateResponse result = apiInstance.getAgentState(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#getAgentState");
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

<a name="getAgentStatuses"></a>
# **getAgentStatuses**
> V1Status getAgentStatuses(owner, uuid)



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
    V1Status result = apiInstance.getAgentStatuses(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#getAgentStatuses");
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

<a name="listAgentNames"></a>
# **listAgentNames**
> V1ListAgentsResponse listAgentNames(owner, offset, limit, sort, query)

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
    V1ListAgentsResponse result = apiInstance.listAgentNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#listAgentNames");
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

<a name="listAgents"></a>
# **listAgents**
> V1ListAgentsResponse listAgents(owner, offset, limit, sort, query)

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
    V1ListAgentsResponse result = apiInstance.listAgents(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#listAgents");
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

<a name="patchAgent"></a>
# **patchAgent**
> V1Agent patchAgent(owner, agentUuid, body)

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
    V1Agent result = apiInstance.patchAgent(owner, agentUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#patchAgent");
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

<a name="syncAgent"></a>
# **syncAgent**
> syncAgent(owner, agentUuid, body)



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
    apiInstance.syncAgent(owner, agentUuid, body);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#syncAgent");
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

<a name="updateAgent"></a>
# **updateAgent**
> V1Agent updateAgent(owner, agentUuid, body)

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
    V1Agent result = apiInstance.updateAgent(owner, agentUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AgentsV1Api#updateAgent");
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

