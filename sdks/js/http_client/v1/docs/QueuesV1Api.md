# PolyaxonSdk.QueuesV1Api

Polyaxon sdk

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



## createQueue

> V1Agent createQueue(owner, agent, body)

Update agent

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let agent = "agent_example"; // String | Agent that consumes the queue
let body = new PolyaxonSdk.V1Queue(); // V1Queue | Queue body
apiInstance.createQueue(owner, agent, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


## deleteQueue

> deleteQueue(owner, agent, uuid)

Sync agent

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let agent = "agent_example"; // String | Agent managing the resource
let uuid = "uuid_example"; // String | Uuid identifier of the entity
apiInstance.deleteQueue(owner, agent, uuid, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
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

- **Content-Type**: Not defined
- **Accept**: application/json


## getQueue

> V1Queue getQueue(owner, agent, uuid)

Patch agent

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let agent = "agent_example"; // String | Agent managing the resource
let uuid = "uuid_example"; // String | Uuid identifier of the entity
apiInstance.getQueue(owner, agent, uuid, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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

- **Content-Type**: Not defined
- **Accept**: application/json


## listOrganizationQueueNames

> V1ListQueuesResponse listOrganizationQueueNames(owner, opts)

List agents names

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};
apiInstance.listOrganizationQueueNames(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listOrganizationQueues

> V1ListQueuesResponse listOrganizationQueues(owner, opts)

List agents

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};
apiInstance.listOrganizationQueues(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listQueueNames

> V1ListQueuesResponse listQueueNames(owner, agent, opts)

Create agent

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let agent = "agent_example"; // String | Agent man managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};
apiInstance.listQueueNames(owner, agent, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **agent** | **String**| Agent man managing the resource | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listQueues

> V1ListQueuesResponse listQueues(owner, agent, opts)

Get agent

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let agent = "agent_example"; // String | Agent man managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};
apiInstance.listQueues(owner, agent, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **agent** | **String**| Agent man managing the resource | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListQueuesResponse**](V1ListQueuesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## patchQueue

> V1Queue patchQueue(owner, queue_agent, queue_uuid, body)

Get State (queues/runs)

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let queue_agent = "queue_agent_example"; // String | Agent
let queue_uuid = "queue_uuid_example"; // String | UUID
let body = new PolyaxonSdk.V1Queue(); // V1Queue | Queue body
apiInstance.patchQueue(owner, queue_agent, queue_uuid, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **queue_agent** | **String**| Agent | 
 **queue_uuid** | **String**| UUID | 
 **body** | [**V1Queue**](V1Queue.md)| Queue body | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateQueue

> V1Queue updateQueue(owner, queue_agent, queue_uuid, body)

Delete agent

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.QueuesV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let queue_agent = "queue_agent_example"; // String | Agent
let queue_uuid = "queue_uuid_example"; // String | UUID
let body = new PolyaxonSdk.V1Queue(); // V1Queue | Queue body
apiInstance.updateQueue(owner, queue_agent, queue_uuid, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **queue_agent** | **String**| Agent | 
 **queue_uuid** | **String**| UUID | 
 **body** | [**V1Queue**](V1Queue.md)| Queue body | 

### Return type

[**V1Queue**](V1Queue.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

