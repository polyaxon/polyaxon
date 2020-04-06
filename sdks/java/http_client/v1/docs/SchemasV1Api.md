# SchemasV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**noOp**](SchemasV1Api.md#noOp) | **GET** /schemas | List teams names


<a name="noOp"></a>
# **noOp**
> V1Schemas noOp()

List teams names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SchemasV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SchemasV1Api apiInstance = new SchemasV1Api();
try {
    V1Schemas result = apiInstance.noOp();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SchemasV1Api#noOp");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1Schemas**](V1Schemas.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

