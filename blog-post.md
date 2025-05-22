# Building Multi-Language SDKs from a Single OpenAPI Specification with Wirespec

## Introduction

In today's API-driven world, providing high-quality Software Development Kits (SDKs) for your API is crucial for developer adoption and success. However, maintaining multiple SDKs across different programming languages can be a significant challenge. Each SDK needs to be updated whenever the API changes, and ensuring consistency across all implementations is often difficult and error-prone.

In this blog post, we'll explore how we tackled this challenge by using Wirespec to generate consistent SDKs for the Bunq API across four different programming languages: Java, Kotlin, Python, and TypeScript, all from a single OpenAPI specification.

## The Challenge

When building SDKs for multiple programming languages, developers typically face several challenges:

1. **Consistency**: Ensuring that all SDKs behave the same way and provide the same features.
2. **Maintenance**: Updating all SDKs whenever the API changes.
3. **Language-specific idioms**: Making sure each SDK feels natural to use in its target language.
4. **Documentation**: Keeping documentation in sync across all SDKs.

## Enter Wirespec

[Wirespec](https://wirespec.dev/) is a powerful tool that allows us to generate SDKs from an OpenAPI specification. It's a pure functional and dependency-free model that can generate code for multiple programming languages while ensuring consistency across all implementations.

With Wirespec, we can:

1. Define our API once using the OpenAPI specification.
2. Generate SDKs for multiple programming languages.
3. Ensure that all SDKs follow the same structure and behavior.
4. Easily update all SDKs when the API changes.

## Our Approach

For the Bunq API, we created a proof of concept (POC) that demonstrates how Wirespec can be used to generate SDKs for four different programming languages: Java, Kotlin, Python, and TypeScript.

### The Architecture

Our architecture consists of several key components:

1. **OpenAPI Specification**: We start with a single OpenAPI specification (openapi.json) that defines the Bunq API.
2. **Wirespec**: We use Wirespec to generate the core SDK code for each language.
3. **Common Components**: Each SDK includes common components such as:
   - **Signing Logic**: For authenticating API requests.
   - **Context Model**: For managing API context (e.g., session tokens, user IDs).
   - **Client**: For making HTTP requests to the API.

### The Implementation

Let's take a look at how each SDK is implemented:

#### Java SDK

The Java SDK uses Wirespec to generate endpoint classes and models from the OpenAPI specification. It provides a clean, type-safe API for interacting with the Bunq API:

```java
READ_User.Request req = new READ_User.Request(
    context.getUserId(),
    Optional.empty(),
    config.getServiceName(),
    Optional.empty(),
    Optional.empty(),
    Optional.empty(),
    Optional.empty(),
    config.getApiKey()
);

READ_User.Response<?> res = client.rEAD_User(req).get();

if (res instanceof READ_User.Response200 response) {
    String legalName = response.getBody().UserPerson().flatMap(UserPerson::legal_name).orElseThrow();
    // Use the legal name
}
```

#### Kotlin SDK

The Kotlin SDK leverages Kotlin's modern features to provide a concise and idiomatic API:

```kotlin
val request = READ_User.Request(
    itemId = context.userId,
    CacheControl = null,
    UserAgent = context.serviceName,
    XBunqLanguage = null,
    XBunqRegion = null,
    XBunqClientRequestId = null,
    XBunqGeolocation = null,
    XBunqClientAuthentication = context.sessionToken
)

val response = client.rEAD_User(request)

when (response) {
    is READ_User.Response200 -> {
        val displayName = response.body.UserPerson?.display_name
        // Use the display name
    }
    else -> throw RuntimeException("Cannot read user")
}
```

#### Python SDK

The Python SDK uses modern Python features like pattern matching to provide a clean and Pythonic API:

```python
req = READ_User.Request(
    CacheControl = None,
    UserAgent = context.service_name,
    XBunqLanguage = None,
    XBunqRegion = None,
    XBunqClientRequestId = None,
    XBunqGeolocation = None,
    XBunqClientAuthentication = context.session_token,
)

res = sdk.READ_User(itemId = context.user_id)

match res:
    case READ_User.Response200(body):
        if body.UserPerson is None: raise Exception("User not found")
        display_name = body.UserPerson.display_name
        # Use the display name
```

#### TypeScript SDK

The TypeScript SDK uses modern JavaScript/TypeScript features like async/await to provide a clean and idiomatic API:

```typescript
const req = READ_User.request({
    "Cache-Control": undefined,
    "User-Agent": context.serverName,
    "X-Bunq-Client-Authentication": context.sessionToken,
    "X-Bunq-Client-Request-Id": undefined,
    "X-Bunq-Geolocation": undefined,
    "X-Bunq-Language": undefined,
    "X-Bunq-Region": undefined,
    "itemId": context.userId
})

const res = await client(context).rEAD_User(req)

if(res.status === 200) {
    const displayName = res.body.UserPerson?.display_name
    // Use the display name
} else {
    throw new Error("Cannot read user")
}
```

## Benefits

Using Wirespec to generate SDKs from a single OpenAPI specification offers several benefits:

1. **Consistency**: All SDKs follow the same structure and behavior, making it easier for developers to switch between languages.
2. **Maintenance**: When the API changes, we only need to update the OpenAPI specification, and all SDKs can be regenerated automatically.
3. **Type Safety**: All SDKs provide type-safe APIs, reducing the risk of runtime errors.
4. **Documentation**: Documentation can be generated from the OpenAPI specification, ensuring that it's always in sync with the actual API.
5. **Language-specific idioms**: Each SDK feels natural to use in its target language, thanks to Wirespec's language-specific code generation.

## Conclusion

Building and maintaining SDKs for multiple programming languages can be a significant challenge, but tools like Wirespec make it much easier. By generating SDKs from a single OpenAPI specification, we can ensure consistency, reduce maintenance overhead, and provide a better developer experience.

Our proof of concept for the Bunq API demonstrates that this approach is viable and offers significant benefits. We encourage you to explore Wirespec and consider using it for your own API SDKs.

## Resources

- [Wirespec Documentation](https://wirespec.dev/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Bunq API Documentation](https://doc.bunq.com/)