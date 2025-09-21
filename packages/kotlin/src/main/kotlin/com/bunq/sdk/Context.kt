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
import com.bunq.sdk.generated.model.UserApiKey
import com.bunq.sdk.generated.model.UserApiKeyAnchoredUser
import java.time.Instant

data class Context(
    val serverPublicKey: String,
    val deviceId: Long,
    val sessionId: Long,
    val sessionToken: String,
    val userId: Long,
    val sessionExpiryTime: Instant,
    val installationToken: String,
    val config: Config
)

/**
 * Refresh this context's session.
 * This recreates the session with the same device and installation but gets a new session token.
 *
 * @return A new Context with refreshed session information
 */
fun Context.refreshSession(): Context {
    val serverSession = createSessionServer(
        token = installationToken,
        config = config
    )

    val sessionTimeoutSeconds = serverSession.getSessionTimeout()
        ?: run {
            println("No session timeout found in session server response, using default of 30 minutes")
            30 * 60L
        }
    val sessionExpiryTime = sessionTimeoutSeconds.let {
        Instant.now().plusSeconds(it)
    }

    return this.copy(
        sessionId = serverSession.Id?.id ?: error("No session id"),
        sessionToken = serverSession.Token?.token ?: error("No session token"),
        userId = serverSession.getUserId(),
        sessionExpiryTime = sessionExpiryTime,
    )
}

fun initContext(config: Config): Context {
    val installation = createInstallation(config)
    if (installation.Token?.token == null) error("Token not available")
    val deviceServer = createDeviceServer(installation.Token.token, config)
    val serverSession = createSessionServer(installation.Token.token, config)

    val sessionTimeoutSeconds: Long = serverSession.getSessionTimeout() ?: run {
        println("No session timeout found in session server response, using default of 30 minutes")
        30 * 60L
    }

    val sessionExpiryTime = sessionTimeoutSeconds.let {
        Instant.now().plusSeconds(it)
    }

    return Context(
        serverPublicKey = installation.ServerPublicKey?.server_public_key ?: error("No server public key"),
        deviceId = deviceServer.Id?.id ?: error("No device id"),
        sessionId = serverSession.Id?.id ?: error("No session id"),
        sessionToken = serverSession.Token?.token ?: error("No session token"),
        userId = serverSession.getUserId(),
        sessionExpiryTime = sessionExpiryTime,
        installationToken = installation.Token.token,
        config = config
    )
}

private fun createInstallation(config: Config): InstallationCreate {
    val body = Installation(
        client_public_key = config.signingKeys.publicKeyAsPem()
    )
    val request = CREATE_Installation.Request(
        body = body,
    )

    val rawRequest = CREATE_Installation.toRequest(serialization, request)
    val rawResponse = send(config, rawRequest)
    val res = CREATE_Installation.fromResponse(serialization, rawResponse)

    when (res) {
        is CREATE_Installation.Response200 -> return res.body
        is CREATE_Installation.Response400 -> error("Cannot create installation")
    }
}

fun createDeviceServer(token: String, config: Config): DeviceServerCreate {
    val body = DeviceServer(
        description = config.serviceName,
        secret = config.apiKey,
        permitted_ips = listOf("*")
    )
    val request = CREATE_DeviceServer.Request(
        body = body,
    )

    val rawRequest = CREATE_DeviceServer.toRequest(serialization, request)
    val authRequest = rawRequest.copy(headers = rawRequest.headers + ("X-Bunq-Client-Authentication" to listOf(token)))
    val rawResponse = send(config, authRequest)
    val res = CREATE_DeviceServer.fromResponse(serialization, rawResponse)

    when (res) {
        is CREATE_DeviceServer.Response200 -> return res.body
        is CREATE_DeviceServer.Response400 -> error("Cannot create device server")
    }
}


private fun createSessionServer(
    token: String,
    config: Config
): SessionServerCreate {
    val body = SessionServer(
        secret = config.apiKey,
    )
    val request = CREATE_SessionServer.Request(
        body = body,
    )

    val rawRequest = CREATE_SessionServer.toRequest(serialization, request)
    val authRequest = rawRequest.copy(
        headers = rawRequest.headers + ("UserAgent" to listOf(config.serviceName)) + ("X-Bunq-Client-Authentication" to listOf(
            token
        ))
    )
    val rawResponse = send(config, authRequest)

    val res = CREATE_SessionServer.fromResponse(serialization, rawResponse)

    when (res) {
        is CREATE_SessionServer.Response200 -> return res.body
        is CREATE_SessionServer.Response400 -> error("Cannot create session server")
    }
}

/**
 * Sessions can be for various types of users, of which only one is filled.
 */
private fun SessionServerCreate.getUserId(): Long {
    return UserPerson?.id
        ?: UserCompany?.id
        ?: UserApiKey?.id
        ?: UserPaymentServiceProvider?.id
        ?: error("No user id found in the SessionServerCreate response")
}

/**
 * Extract session timeout from the user in the SessionServerCreate response.
 */
private fun SessionServerCreate.getSessionTimeout(): Long? =
    UserPerson?.session_timeout
        ?: UserCompany?.session_timeout
        ?: UserPaymentServiceProvider?.session_timeout
        ?: UserApiKey?.getSessionTimeout()

private fun UserApiKey.getSessionTimeout(): Long? =
    granted_by_user?.getSessionTimeout()
        ?: requested_by_user?.getSessionTimeout()

private fun UserApiKeyAnchoredUser.getSessionTimeout(): Long? =
    UserPerson?.session_timeout
        ?: UserCompany?.session_timeout
        ?: UserPaymentServiceProvider?.session_timeout