# Bunq SDK Generator

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

## Using the SDKs

Each SDK provides a consistent API for interacting with the Bunq API. The generated code includes:

- Model classes for all API objects
- Endpoint definitions for all API endpoints
- A `Sdk` class that provides a unified interface for making API calls

## Contributing

If you want to modify the SDKs:

1. Update the OpenAPI specification (`openapi.json`) if needed
2. Modify the custom emitters in the build files if you need to change the structure of the generated code
3. Run the build to regenerate the SDKs
4. Test the changes to ensure they work as expected

## License

This project is licensed under the terms of the LICENSE file included in the repository.