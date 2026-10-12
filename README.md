# Bunq SDK

> ⚠️ **Warning**: This repository is not affiliated with Bunq. It is a research project by Flock. For more information,
> please see our [blog post](https://wirespec.io/blog/bunq-sdk).



This repository showcases how four different SDKs (Java, Kotlin, TypeScript/JavaScript, and Python) are generated from a single OpenAPI specification using Wirespec. All projects follow the same structure and build process, demonstrating the power of code generation for maintaining consistent APIs across multiple programming languages.

## Overview

The repository contains:

- A single OpenAPI specification (`openapi.json`) in the root directory
- Four SDK packages in the `packages` directory:
  - Java SDK
  - Kotlin SDK
  - NPM (TypeScript/JavaScript) SDK
  - Python SDK
- Custom build logic in the `buildSrc` directory
- Gradle build configuration for all packages

## How It Works

### OpenAPI Specification

The repository uses a single OpenAPI specification (`openapi.json`) as the source of truth for all SDKs. This ensures that all SDKs have consistent API definitions, models, and endpoints.

### Wirespec

[Wirespec](https://github.com/flock-community/wirespec) is used to generate code from the OpenAPI specification. Wirespec is a language and code generation tool that can generate client libraries for multiple programming languages from a single specification.

Each SDK package uses the Wirespec Gradle plugin to:
1. Read the OpenAPI specification
2. Apply custom pre-processing (via `OpenApiPreProcessor`)
3. Generate code using a custom emitter class
4. Include the generated code in the build

## Requirements

- Kotlin package: Kotlin 2.3+, Wirespec 0.21.x runtime, JVM 17+; consumers bring their own kotlinx-coroutines (the client functions are `suspend`)
- Java package: not available in this release (being ported to Wirespec 0.21)

## Using the SDKs

Each SDK provides a consistent API for interacting with the Bunq API. The generated code includes:

- Model classes for all API objects
- Endpoint definitions for all API endpoints
- A `Context` class that manages authentication and session state

### Session Management

All SDKs provide session management capabilities to handle authentication and session expiry with the Bunq API:

- **Session Creation**: Initialize a context with API credentials to establish a session
- **Session Expiry Tracking**: Monitor when sessions will expire 
- **Session Refresh**: Renew sessions before they expire to maintain API access

For detailed session management documentation for each language, see:

- [Java Session Management](docs/java.md)
- [Kotlin Session Management](docs/kotlin.md)
- [TypeScript/npm Session Management](docs/typescript.md)
- [Python Session Management](docs/python.md)

**Quick Examples:**

Java:
```java
Context context = Context.initContext(config);
Instant expiryTime = context.sessionExpiryTime();
Context refreshedContext = context.refreshSession();
```

Kotlin:
```kotlin
val context = initContext(config)
val expiryTime: Instant = context.sessionExpiryTime
val refreshedContext = context.refreshSession()
```

TypeScript:
```typescript
const context = await initContext(config);
const expiryTime: Date = context.sessionExpiryTime;
const refreshedContext = await refreshSession(context);
```

Python:
```python
context = init_context(config)
expiry_time = context.session_expiry_time
refreshed_context = refresh_session(context)
```

## Contributing

If you want to modify the SDKs:

1. Update the OpenAPI specification (`openapi.json`) if needed
2. Modify the custom emitters in the build files if you need to change the structure of the generated code
3. Run the build to regenerate the SDKs
4. Test the changes to ensure they work as expected

## License

This project is licensed under the terms of the LICENSE file included in the repository.