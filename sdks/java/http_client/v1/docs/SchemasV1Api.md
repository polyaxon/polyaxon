# SchemasV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**schemasV1NoOp**](SchemasV1Api.md#schemasV1NoOp) | **GET** /schemas | List teams names


<a name="schemasV1NoOp"></a>
# **schemasV1NoOp**
> V1Schemas schemasV1NoOp()

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
    V1Schemas result = apiInstance.schemasV1NoOp();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SchemasV1Api#schemasV1NoOp");
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

