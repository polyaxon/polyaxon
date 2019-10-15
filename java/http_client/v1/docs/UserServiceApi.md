# UserServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getUser**](UserServiceApi.md#getUser) | **GET** /api/v1/users | List runs


<a name="getUser"></a>
# **getUser**
> V1User getUser()

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.UserServiceApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

UserServiceApi apiInstance = new UserServiceApi();
try {
    V1User result = apiInstance.getUser();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling UserServiceApi#getUser");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1User**](V1User.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

