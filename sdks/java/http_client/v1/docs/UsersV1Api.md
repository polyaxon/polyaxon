# UsersV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**usersV1GetUser**](UsersV1Api.md#usersV1GetUser) | **GET** /api/v1/users | Login


<a name="usersV1GetUser"></a>
# **usersV1GetUser**
> V1User usersV1GetUser()

Login

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.UsersV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

UsersV1Api apiInstance = new UsersV1Api();
try {
    V1User result = apiInstance.usersV1GetUser();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling UsersV1Api#usersV1GetUser");
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

