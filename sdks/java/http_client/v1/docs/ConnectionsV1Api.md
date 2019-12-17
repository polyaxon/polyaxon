# ConnectionsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createConnection**](ConnectionsV1Api.md#createConnection) | **POST** /api/v1/orgs/{owner}/connections | List runs
[**deleteConnection**](ConnectionsV1Api.md#deleteConnection) | **DELETE** /api/v1/orgs/{owner}/connections/{uuid} | Patch run
[**getConnection**](ConnectionsV1Api.md#getConnection) | **GET** /api/v1/orgs/{owner}/connections/{uuid} | Create new run
[**listConnectionNames**](ConnectionsV1Api.md#listConnectionNames) | **GET** /api/v1/orgs/{owner}/connections/names | List bookmarked runs for user
[**listConnections**](ConnectionsV1Api.md#listConnections) | **GET** /api/v1/orgs/{owner}/connections | List archived runs for user
[**patchConnection**](ConnectionsV1Api.md#patchConnection) | **PATCH** /api/v1/orgs/{owner}/connections/{connection.uuid} | Update run
[**updateConnection**](ConnectionsV1Api.md#updateConnection) | **PUT** /api/v1/orgs/{owner}/connections/{connection.uuid} | Get run


<a name="createConnection"></a>
# **createConnection**
> V1Connection createConnection(owner, body)

List runs

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
V1Connection body = new V1Connection(); // V1Connection | Connection body
try {
    V1Connection result = apiInstance.createConnection(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#createConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1Connection**](V1Connection.md)| Connection body |

### Return type

[**V1Connection**](V1Connection.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteConnection"></a>
# **deleteConnection**
> deleteConnection(owner, uuid)

Patch run

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
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteConnection(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#deleteConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getConnection"></a>
# **getConnection**
> V1Connection getConnection(owner, uuid)

Create new run

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
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1Connection result = apiInstance.getConnection(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#getConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1Connection**](V1Connection.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listConnectionNames"></a>
# **listConnectionNames**
> V1ListConnectionsResponse listConnectionNames(owner, offset, limit, sort, query)

List bookmarked runs for user

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
    V1ListConnectionsResponse result = apiInstance.listConnectionNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#listConnectionNames");
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

<a name="listConnections"></a>
# **listConnections**
> V1ListConnectionsResponse listConnections(owner, offset, limit, sort, query)

List archived runs for user

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
    V1ListConnectionsResponse result = apiInstance.listConnections(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#listConnections");
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

<a name="patchConnection"></a>
# **patchConnection**
> V1Connection patchConnection(owner, connectionUuid, body)

Update run

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
V1Connection body = new V1Connection(); // V1Connection | Connection body
try {
    V1Connection result = apiInstance.patchConnection(owner, connectionUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#patchConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **connectionUuid** | **String**| UUID |
 **body** | [**V1Connection**](V1Connection.md)| Connection body |

### Return type

[**V1Connection**](V1Connection.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateConnection"></a>
# **updateConnection**
> V1Connection updateConnection(owner, connectionUuid, body)

Get run

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
V1Connection body = new V1Connection(); // V1Connection | Connection body
try {
    V1Connection result = apiInstance.updateConnection(owner, connectionUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConnectionsV1Api#updateConnection");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **connectionUuid** | **String**| UUID |
 **body** | [**V1Connection**](V1Connection.md)| Connection body |

### Return type

[**V1Connection**](V1Connection.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

