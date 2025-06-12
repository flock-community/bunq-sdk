package com.bunq.sdk

import com.bunq.sdk.generated.endpoint.CREATE_DeviceServer
import com.bunq.sdk.generated.endpoint.CREATE_Installation
import com.bunq.sdk.generated.endpoint.CREATE_SessionServer
import com.bunq.sdk.generated.model.DeviceServer
import com.bunq.sdk.generated.model.DeviceServerCreate
import com.bunq.sdk.generated.model.Installation
import com.bunq.sdk.generated.model.InstallationCreate
import com.bunq.sdk.generated.model.SessionServer
import com.bunq.sdk.generated.model.SessionServerCreate

data class Context(
    val apiKey: String,
    val serviceName: String,
    val serverPublicKey: String,
    val deviceId: Long,
    val sessionId: Long,
    val sessionToken: String,
    val userId: Long,
    val userAgent: String? = null,
    val cacheControl: String? = null,
    val language: String? = null,
    val region: String? = null,
    val clientRequestId: String? = null,
    val geolocation: String? = null,
)

fun initContext(config: Config): Context {

    val signing = Signing(config)

    fun createInstallation(serviceName: String, publicKeyPem: String): InstallationCreate {
        val body = Installation(
            client_public_key = publicKeyPem
        )
        val request = CREATE_Installation.Request(
            body = body,
        )

        val rawRequest = CREATE_Installation.toRequest(serialization, request)
        val rawResponse = send(signing, rawRequest)
        val res = CREATE_Installation.fromResponse(serialization, rawResponse)

        when (res) {
            is CREATE_Installation.Response200 -> return res.body
            is CREATE_Installation.Response400 -> error("Cannot create installation")
        }
    }

    fun createDeviceServer(serviceName: String, apiKey: String, token: String): DeviceServerCreate {
        val body = DeviceServer(
            description = serviceName,
            secret = apiKey,
            permitted_ips = listOf("*")
        )
        val request = CREATE_DeviceServer.Request(
            body = body,
        )

        val rawRequest = CREATE_DeviceServer.toRequest(serialization, request)
        val authRequest = rawRequest.copy(headers = rawRequest.headers + ("X-Bunq-Client-Authentication" to listOf(token)))
        val rawResponse = send(signing, authRequest)
        val res = CREATE_DeviceServer.fromResponse(serialization, rawResponse)

        when (res) {
            is CREATE_DeviceServer.Response200 -> return res.body
            is CREATE_DeviceServer.Response400 -> error("Cannot create device server")
        }
    }

    fun createSessionServer(serviceName: String, apiKey: String, token: String): SessionServerCreate {
        val body = SessionServer(
            secret = apiKey,
        )
        val request = CREATE_SessionServer.Request(
            body = body,
        )

        val rawRequest = CREATE_SessionServer.toRequest(serialization, request)
        val authRequest = rawRequest.copy(headers = rawRequest.headers + ("UserAgent" to listOf(serviceName)) +  ("X-Bunq-Client-Authentication" to listOf(token)))
        val rawResponse = send(signing, authRequest)

        val res = CREATE_SessionServer.fromResponse(serialization, rawResponse)

        when (res) {
            is CREATE_SessionServer.Response200 -> return res.body
            is CREATE_SessionServer.Response400 -> error("Cannot create session server")
        }
    }

    val (_, publicKeyPem) = signing.generateRsaKeyPair()
    val installation = createInstallation(config.serviceName, publicKeyPem)
    if (installation.Token?.token == null) error("Token not available")
    val deviceServer = createDeviceServer(config.serviceName, config.apiKey, installation.Token.token)
    val serverSession = createSessionServer(config.serviceName, config.apiKey, installation.Token.token)
    return Context(
        apiKey = config.apiKey,
        serviceName = config.serviceName,
        serverPublicKey = installation.ServerPublicKey?.server_public_key ?: error("No server public key"),
        deviceId = deviceServer.id ?: error("No device id"),
        sessionId = serverSession.Id?.id ?: error("No session id"),
        sessionToken = serverSession.Token?.token ?: error("No session token"),
        userId = serverSession.UserPerson?.id ?: error("No user id"),
        userAgent = config.userAgent,
        cacheControl = config.cacheControl,
        language = config.language,
        region = config.region,
        clientRequestId = config.clientRequestId,
        geolocation = config.geolocation,
    )
}