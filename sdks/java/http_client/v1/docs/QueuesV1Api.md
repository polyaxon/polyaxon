# QueuesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**queuesV1CreateQueue**](QueuesV1Api.md#queuesV1CreateQueue) | **POST** /api/v1/orgs/{owner}/agents/{agent}/queues | Update agent
[**queuesV1DeleteQueue**](QueuesV1Api.md#queuesV1DeleteQueue) | **DELETE** /api/v1/orgs/{owner}/agents/{agent}/queues/{uuid} | Sync agent
[**queuesV1GetQueue**](QueuesV1Api.md#queuesV1GetQueue) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues/{uuid} | Patch agent
[**queuesV1ListOrganizationQueueNames**](QueuesV1Api.md#queuesV1ListOrganizationQueueNames) | **GET** /api/v1/orgs/{owner}/queues/names | List agents names
[**queuesV1ListOrganizationQueues**](QueuesV1Api.md#queuesV1ListOrganizationQueues) | **GET** /api/v1/orgs/{owner}/queues | List agents
[**queuesV1ListQueueNames**](QueuesV1Api.md#queuesV1ListQueueNames) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues/names | Create agent
[**queuesV1ListQueues**](QueuesV1Api.md#queuesV1ListQueues) | **GET** /api/v1/orgs/{owner}/agents/{agent}/queues | Get agent
[**queuesV1PatchQueue**](QueuesV1Api.md#queuesV1PatchQueue) | **PATCH** /api/v1/orgs/{owner}/agents/{queue.agent}/queues/{queue.uuid} | Get State (queues/runs)
[**queuesV1UpdateQueue**](QueuesV1Api.md#queuesV1UpdateQueue) | **PUT** /api/v1/orgs/{owner}/agents/{queue.agent}/queues/{queue.uuid} | Delete agent


<a name="queuesV1CreateQueue"></a>
# **queuesV1CreateQueue**
> V1Agent queuesV1CreateQueue(owner, agent, body)

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
    V1Agent result = apiInstance.queuesV1CreateQueue(owner, agent, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1CreateQueue");
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

<a name="queuesV1DeleteQueue"></a>
# **queuesV1DeleteQueue**
> queuesV1DeleteQueue(owner, agent, uuid)

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
    apiInstance.queuesV1DeleteQueue(owner, agent, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1DeleteQueue");
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

<a name="queuesV1GetQueue"></a>
# **queuesV1GetQueue**
> V1Queue queuesV1GetQueue(owner, agent, uuid)

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
    V1Queue result = apiInstance.queuesV1GetQueue(owner, agent, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1GetQueue");
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

<a name="queuesV1ListOrganizationQueueNames"></a>
# **queuesV1ListOrganizationQueueNames**
> V1ListQueuesResponse queuesV1ListOrganizationQueueNames(owner, offset, limit, sort, query)

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
    V1ListQueuesResponse result = apiInstance.queuesV1ListOrganizationQueueNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1ListOrganizationQueueNames");
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

<a name="queuesV1ListOrganizationQueues"></a>
# **queuesV1ListOrganizationQueues**
> V1ListQueuesResponse queuesV1ListOrganizationQueues(owner, offset, limit, sort, query)

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
    V1ListQueuesResponse result = apiInstance.queuesV1ListOrganizationQueues(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1ListOrganizationQueues");
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

<a name="queuesV1ListQueueNames"></a>
# **queuesV1ListQueueNames**
> V1ListQueuesResponse queuesV1ListQueueNames(owner, agent, offset, limit, sort, query)

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
    V1ListQueuesResponse result = apiInstance.queuesV1ListQueueNames(owner, agent, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1ListQueueNames");
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

<a name="queuesV1ListQueues"></a>
# **queuesV1ListQueues**
> V1ListQueuesResponse queuesV1ListQueues(owner, agent, offset, limit, sort, query)

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
    V1ListQueuesResponse result = apiInstance.queuesV1ListQueues(owner, agent, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1ListQueues");
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

<a name="queuesV1PatchQueue"></a>
# **queuesV1PatchQueue**
> V1Queue queuesV1PatchQueue(owner, queueAgent, queueUuid, body)

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
    V1Queue result = apiInstance.queuesV1PatchQueue(owner, queueAgent, queueUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1PatchQueue");
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

<a name="queuesV1UpdateQueue"></a>
# **queuesV1UpdateQueue**
> V1Queue queuesV1UpdateQueue(owner, queueAgent, queueUuid, body)

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
    V1Queue result = apiInstance.queuesV1UpdateQueue(owner, queueAgent, queueUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling QueuesV1Api#queuesV1UpdateQueue");
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

