# ConnectionsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**connectionsV1CreateConnection**](ConnectionsV1Api.md#connectionsV1CreateConnection) | **POST** /api/v1/orgs/{owner}/connections | Create connection
[**connectionsV1DeleteConnection**](ConnectionsV1Api.md#connectionsV1DeleteConnection) | **DELETE** /api/v1/orgs/{owner}/connections/{uuid} | Delete connection
[**connectionsV1GetConnection**](ConnectionsV1Api.md#connectionsV1GetConnection) | **GET** /api/v1/orgs/{owner}/connections/{uuid} | Get connection
[**connectionsV1ListConnectionNames**](ConnectionsV1Api.md#connectionsV1ListConnectionNames) | **GET** /api/v1/orgs/{owner}/connections/names | List connections names
[**connectionsV1ListConnections**](ConnectionsV1Api.md#connectionsV1ListConnections) | **GET** /api/v1/orgs/{owner}/connections | List connections
[**connectionsV1PatchConnection**](ConnectionsV1Api.md#connectionsV1PatchConnection) | **PATCH** /api/v1/orgs/{owner}/connections/{connection.uuid} | Patch connection
[**connectionsV1UpdateConnection**](ConnectionsV1Api.md#connectionsV1UpdateConnection) | **PUT** /api/v1/orgs/{owner}/connections/{connection.uuid} | Update connection


<a name="connectionsV1CreateConnection"></a>
# **connectionsV1CreateConnection**
> V1ConnectionResponse connectionsV1CreateConnection(owner, body)

Create connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1ConnectionResponse body = new V1ConnectionResponse(); // V1ConnectionResponse | Connection body
try {
    V1ConnectionResponse result = apiInstance.connectionsV1CreateConnection(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#connectionsV1CreateConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body |

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1DeleteConnection"></a>
# **connectionsV1DeleteConnection**
> connectionsV1DeleteConnection(owner, uuid)

Delete connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.connectionsV1DeleteConnection(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#connectionsV1DeleteConnection");
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

<a name="connectionsV1GetConnection"></a>
# **connectionsV1GetConnection**
> V1ConnectionResponse connectionsV1GetConnection(owner, uuid)

Get connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1ConnectionResponse result = apiInstance.connectionsV1GetConnection(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#connectionsV1GetConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1ListConnectionNames"></a>
# **connectionsV1ListConnectionNames**
> V1ListConnectionsResponse connectionsV1ListConnectionNames(owner, offset, limit, sort, query)

List connections names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListConnectionsResponse result = apiInstance.connectionsV1ListConnectionNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#connectionsV1ListConnectionNames");
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

[**V1ListConnectionsResponse**](V1ListConnectionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1ListConnections"></a>
# **connectionsV1ListConnections**
> V1ListConnectionsResponse connectionsV1ListConnections(owner, offset, limit, sort, query)

List connections

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListConnectionsResponse result = apiInstance.connectionsV1ListConnections(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#connectionsV1ListConnections");
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

[**V1ListConnectionsResponse**](V1ListConnectionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1PatchConnection"></a>
# **connectionsV1PatchConnection**
> V1ConnectionResponse connectionsV1PatchConnection(owner, connectionUuid, body)

Patch connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String connectionUuid = "connectionUuid_example"; // String | UUID
V1ConnectionResponse body = new V1ConnectionResponse(); // V1ConnectionResponse | Connection body
try {
    V1ConnectionResponse result = apiInstance.connectionsV1PatchConnection(owner, connectionUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#connectionsV1PatchConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **connectionUuid** | **String**| UUID |
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body |

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1UpdateConnection"></a>
# **connectionsV1UpdateConnection**
> V1ConnectionResponse connectionsV1UpdateConnection(owner, connectionUuid, body)

Update connection

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConnectionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConnectionsV1Api apiInstance = new ConnectionsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String connectionUuid = "connectionUuid_example"; // String | UUID
V1ConnectionResponse body = new V1ConnectionResponse(); // V1ConnectionResponse | Connection body
try {
    V1ConnectionResponse result = apiInstance.connectionsV1UpdateConnection(owner, connectionUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#connectionsV1UpdateConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **connectionUuid** | **String**| UUID |
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body |

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

