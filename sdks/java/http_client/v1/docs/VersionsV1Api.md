# VersionsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**versionsV1GetLogHandler**](VersionsV1Api.md#versionsV1GetLogHandler) | **GET** /api/v1/log_handler | 
[**versionsV1GetVersions**](VersionsV1Api.md#versionsV1GetVersions) | **GET** /api/v1/version | Get current user


<a name="versionsV1GetLogHandler"></a>
# **versionsV1GetLogHandler**
> V1LogHandler versionsV1GetLogHandler()



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.VersionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

VersionsV1Api apiInstance = new VersionsV1Api();
try {
    V1LogHandler result = apiInstance.versionsV1GetLogHandler();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling VersionsV1Api#versionsV1GetLogHandler");
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

<a name="versionsV1GetVersions"></a>
# **versionsV1GetVersions**
> V1Versions versionsV1GetVersions()

Get current user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.VersionsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

VersionsV1Api apiInstance = new VersionsV1Api();
try {
    V1Versions result = apiInstance.versionsV1GetVersions();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling VersionsV1Api#versionsV1GetVersions");
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

