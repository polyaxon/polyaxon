# QueuesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createQueue**](QueuesV1Api.md#createQueue) | **POST** /api/v1/orgs/{owner}/agents/{agent}/queues | Update agent
[**deleteQueue**](QueuesV1Api.md#deleteQueue) | **DELETE** /api/v1/orgs/{owner}/agents/{agent}/queues/{uuid} | Sync agent
[**getQueue**](QueuesV1Api.md#getQueue) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues/{uuid} | Patch agent
[**listOrganizationQueueNames**](QueuesV1Api.md#listOrganizationQueueNames) | **GET** /api/v1/orgs/{owner}/queues/names | List agents names
[**listOrganizationQueues**](QueuesV1Api.md#listOrganizationQueues) | **GET** /api/v1/orgs/{owner}/queues | List agents
[**listQueueNames**](QueuesV1Api.md#listQueueNames) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues/names | Create agent
[**listQueues**](QueuesV1Api.md#listQueues) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues | Get agent
[**patchQueue**](QueuesV1Api.md#patchQueue) | **PATCH** /api/v1/orgs/{owner}/agents/{queue.agent}/queues/{queue.uuid} | Get State (queues/runs)
[**updateQueue**](QueuesV1Api.md#updateQueue) | **PUT** /api/v1/orgs/{owner}/agents/{queue.agent}/queues/{queue.uuid} | Delete agent


<a name="createQueue"></a>
# **createQueue**
> V1Agent createQueue(owner, agent, body)

Update agent

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String agent = "agent_example"; // String | Agent that consumes the queue
V1Queue body = new V1Queue(); // V1Queue | Queue body
try {
    V1Agent result = apiInstance.createQueue(owner, agent, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#createQueue");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **agent** | **String**| Agent that consumes the queue |
 **body** | [**V1Queue**](V1Queue.md)| Queue body |

### Return type

[**V1Agent**](V1Agent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteQueue"></a>
# **deleteQueue**
> deleteQueue(owner, agent, uuid)

Sync agent

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String agent = "agent_example"; // String | Agent managing the resource
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.deleteQueue(owner, agent, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#deleteQueue");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **agent** | **String**| Agent managing the resource |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getQueue"></a>
# **getQueue**
> V1Queue getQueue(owner, agent, uuid)

Patch agent

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String agent = "agent_example"; // String | Agent managing the resource
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Queue result = apiInstance.getQueue(owner, agent, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#getQueue");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **agent** | **String**| Agent managing the resource |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listOrganizationQueueNames"></a>
# **listOrganizationQueueNames**
> V1ListQueuesResponse listOrganizationQueueNames(owner, offset, limit, sort, query)

List agents names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListQueuesResponse result = apiInstance.listOrganizationQueueNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#listOrganizationQueueNames");
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

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listOrganizationQueues"></a>
# **listOrganizationQueues**
> V1ListQueuesResponse listOrganizationQueues(owner, offset, limit, sort, query)

List agents

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListQueuesResponse result = apiInstance.listOrganizationQueues(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#listOrganizationQueues");
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

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listQueueNames"></a>
# **listQueueNames**
> V1ListQueuesResponse listQueueNames(owner, agent, offset, limit, sort, query)

Create agent

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String agent = "agent_example"; // String | Agent man managing the resource
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListQueuesResponse result = apiInstance.listQueueNames(owner, agent, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#listQueueNames");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **agent** | **String**| Agent man managing the resource |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listQueues"></a>
# **listQueues**
> V1ListQueuesResponse listQueues(owner, agent, offset, limit, sort, query)

Get agent

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String agent = "agent_example"; // String | Agent man managing the resource
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListQueuesResponse result = apiInstance.listQueues(owner, agent, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#listQueues");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **agent** | **String**| Agent man managing the resource |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchQueue"></a>
# **patchQueue**
> V1Queue patchQueue(owner, queueAgent, queueUuid, body)

Get State (queues/runs)

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String queueAgent = "queueAgent_example"; // String | Agent
String queueUuid = "queueUuid_example"; // String | UUID
V1Queue body = new V1Queue(); // V1Queue | Queue body
try {
    V1Queue result = apiInstance.patchQueue(owner, queueAgent, queueUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#patchQueue");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **queueAgent** | **String**| Agent |
 **queueUuid** | **String**| UUID |
 **body** | [**V1Queue**](V1Queue.md)| Queue body |

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateQueue"></a>
# **updateQueue**
> V1Queue updateQueue(owner, queueAgent, queueUuid, body)

Delete agent

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.QueuesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

QueuesV1Api apiInstance = new QueuesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String queueAgent = "queueAgent_example"; // String | Agent
String queueUuid = "queueUuid_example"; // String | UUID
V1Queue body = new V1Queue(); // V1Queue | Queue body
try {
    V1Queue result = apiInstance.updateQueue(owner, queueAgent, queueUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#updateQueue");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **queueAgent** | **String**| Agent |
 **queueUuid** | **String**| UUID |
 **body** | [**V1Queue**](V1Queue.md)| Queue body |

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

