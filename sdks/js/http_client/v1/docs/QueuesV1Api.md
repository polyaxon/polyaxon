# PolyaxonSdk.QueuesV1Api

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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var agent = "agent_example"; // String | Agent that consumes the queue

var body = new PolyaxonSdk.V1Queue(); // V1Queue | Queue body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.queuesV1CreateQueue(owner, agent, body, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var agent = "agent_example"; // String | Agent managing the resource

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.queuesV1DeleteQueue(owner, agent, uuid, callback);
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
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var agent = "agent_example"; // String | Agent managing the resource

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.queuesV1GetQueue(owner, agent, uuid, callback);
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
> V1ListQueuesResponse queuesV1ListOrganizationQueueNames(owner, opts)

List agents names

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

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
apiInstance.queuesV1ListOrganizationQueueNames(owner, opts, callback);
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

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="queuesV1ListOrganizationQueues"></a>
# **queuesV1ListOrganizationQueues**
> V1ListQueuesResponse queuesV1ListOrganizationQueues(owner, opts)

List agents

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

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
apiInstance.queuesV1ListOrganizationQueues(owner, opts, callback);
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

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="queuesV1ListQueueNames"></a>
# **queuesV1ListQueueNames**
> V1ListQueuesResponse queuesV1ListQueueNames(owner, agent, opts)

Create agent

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var agent = "agent_example"; // String | Agent man managing the resource

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
apiInstance.queuesV1ListQueueNames(owner, agent, opts, callback);
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

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="queuesV1ListQueues"></a>
# **queuesV1ListQueues**
> V1ListQueuesResponse queuesV1ListQueues(owner, agent, opts)

Get agent

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var agent = "agent_example"; // String | Agent man managing the resource

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
apiInstance.queuesV1ListQueues(owner, agent, opts, callback);
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

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="queuesV1PatchQueue"></a>
# **queuesV1PatchQueue**
> V1Queue queuesV1PatchQueue(owner, queue_agent, queue_uuid, body)

Get State (queues/runs)

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var queue_agent = "queue_agent_example"; // String | Agent

var queue_uuid = "queue_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Queue(); // V1Queue | Queue body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.queuesV1PatchQueue(owner, queue_agent, queue_uuid, body, callback);
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

<a name="queuesV1UpdateQueue"></a>
# **queuesV1UpdateQueue**
> V1Queue queuesV1UpdateQueue(owner, queue_agent, queue_uuid, body)

Delete agent

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.QueuesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var queue_agent = "queue_agent_example"; // String | Agent

var queue_uuid = "queue_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Queue(); // V1Queue | Queue body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.queuesV1UpdateQueue(owner, queue_agent, queue_uuid, body, callback);
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

