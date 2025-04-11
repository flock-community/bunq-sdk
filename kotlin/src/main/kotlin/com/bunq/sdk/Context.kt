package com.bunq.sdk

import com.bunq.sdk.generated.CREATE_DeviceServerEndpoint
import com.bunq.sdk.generated.CREATE_InstallationEndpoint
import com.bunq.sdk.generated.CREATE_SessionServerEndpoint
import com.bunq.sdk.generated.DeviceServer
import com.bunq.sdk.generated.DeviceServerCreate
import com.bunq.sdk.generated.Installation
import com.bunq.sdk.generated.InstallationCreate
import com.bunq.sdk.generated.SessionServer
import com.bunq.sdk.generated.SessionServerCreate

data class Context(
    val apiKey: String,
    val serviceName: String,
    val serverPublicKey: String,
    val deviceId: Long,
    val sessionId: Long,
    val sessionToken: String,
    val userId: Long
)

fun initContext(config: Config): Context {

    val signing = Signing(config)

    fun createInstallation(serviceName: String, publicKeyPem: String): InstallationCreate {
        val body = Installation(
            client_public_key = publicKeyPem
        )
        val request = CREATE_InstallationEndpoint.Request(
            CacheControl = null,
            UserAgent = serviceName,
            XBunqLanguage = null,
            XBunqRegion = null,
            XBunqClientRequestId = null,
            XBunqGeolocation = null,
            XBunqClientAuthentication = "",
            body = body,
        )

        val rawRequest = CREATE_InstallationEndpoint.toRequest(serialization, request)
        val rawResponse = send(signing, rawRequest)
        val res = CREATE_InstallationEndpoint.fromResponse(serialization, rawResponse)

        when (res) {
            is CREATE_InstallationEndpoint.Response200 -> return res.body
            is CREATE_InstallationEndpoint.Response400 -> error("Cannot create installation")
        }
    }

     fun createDeviceServer(serviceName: String, apiKey: String, token: String): DeviceServerCreate {
        val body = DeviceServer(
            description = serviceName,
            secret = apiKey,
            permitted_ips = listOf("*")
        )
        val request = CREATE_DeviceServerEndpoint.Request(
            CacheControl = null,
            UserAgent = serviceName,
            XBunqLanguage = null,
            XBunqRegion = null,
            XBunqClientRequestId = null,
            XBunqGeolocation = null,
            XBunqClientAuthentication = token,
            body = body,
        )

        val rawRequest = CREATE_DeviceServerEndpoint.toRequest(serialization, request)
        val rawResponse = send(signing, rawRequest)
        val res =  CREATE_DeviceServerEndpoint.fromResponse(serialization, rawResponse)

        when (res) {
            is CREATE_DeviceServerEndpoint.Response200 -> return res.body
            is CREATE_DeviceServerEndpoint.Response400 -> error("Cannot create device server")
        }
    }

     fun createSessionServer(serviceName: String, apiKey: String, token: String): SessionServerCreate {
        val body = SessionServer(
            secret = apiKey,
        )
        val request = CREATE_SessionServerEndpoint.Request(
            CacheControl = null,
            UserAgent = serviceName,
            XBunqLanguage = null,
            XBunqRegion = null,
            XBunqClientRequestId = null,
            XBunqGeolocation = null,
            XBunqClientAuthentication = token,
            body = body,
        )

        val rawRequest = CREATE_SessionServerEndpoint.toRequest(serialization, request)
        val rawResponse = send(signing, rawRequest)
        val res = CREATE_SessionServerEndpoint.fromResponse(serialization, rawResponse)

        when (res) {
            is CREATE_SessionServerEndpoint.Response200 -> return res.body
            is CREATE_SessionServerEndpoint.Response400 -> error("Cannot create session server")
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
        deviceId = deviceServer.Id?.id ?: error("No device id"),
        sessionId = serverSession.Id?.id ?: error("No session id"),
        sessionToken = serverSession.Token?.token ?: error("No session token"),
        userId = serverSession.UserPerson?.id ?: error("No user id")
    )
}