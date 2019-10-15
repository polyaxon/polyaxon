# VersionServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getLogHandler**](VersionServiceApi.md#getLogHandler) | **GET** /api/v1/log_handler | List bookmarked runs
[**getVersions**](VersionServiceApi.md#getVersions) | **GET** /api/v1/versions | List runs


<a name="getLogHandler"></a>
# **getLogHandler**
> V1LogHandler getLogHandler()

List bookmarked runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.VersionServiceApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

VersionServiceApi apiInstance = new VersionServiceApi();
try {
    V1LogHandler result = apiInstance.getLogHandler();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling VersionServiceApi#getLogHandler");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1LogHandler**](V1LogHandler.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getVersions"></a>
# **getVersions**
> V1Versions getVersions()

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.VersionServiceApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

VersionServiceApi apiInstance = new VersionServiceApi();
try {
    V1Versions result = apiInstance.getVersions();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling VersionServiceApi#getVersions");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1Versions**](V1Versions.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

