package com.bunq.sdk

import com.bunq.sdk.generated.endpoint.CreateDeviceServer
import com.bunq.sdk.generated.endpoint.CreateInstallation
import com.bunq.sdk.generated.endpoint.CreateSessionServer
import com.bunq.sdk.generated.model.DeviceServer
import com.bunq.sdk.generated.model.DeviceServerCreate
import com.bunq.sdk.generated.model.Installation
import com.bunq.sdk.generated.model.InstallationCreate
import com.bunq.sdk.generated.model.SessionServer
import com.bunq.sdk.generated.model.SessionServerCreate
import com.bunq.sdk.generated.model.UserApiKey
import com.bunq.sdk.generated.model.UserApiKeyAnchoredUser
import io.github.oshai.kotlinlogging.KotlinLogging
import java.time.Instant

private val logger = KotlinLogging.logger {}

private fun setupFailure(action: String, description: String?) = "Cannot $action (status 400): $description"

data class Context(
    val serverPublicKey: String,
    val deviceId: Long,
    val sessionId: Long,
    val sessionToken: String,
    val userId: Long,
    val sessionExpiryTime: Instant,
    val installationToken: String,
    val config: Config
) {
    /** Masks sessionToken and installationToken; the object still holds them. config is masked by its own toString. */
    override fun toString(): String =
        "Context(serverPublicKey=$serverPublicKey, deviceId=$deviceId, sessionId=$sessionId, sessionToken=***, " +
            "userId=$userId, sessionExpiryTime=$sessionExpiryTime, installationToken=***, config=$config)"
}

/**
 * Refresh this context's session.
 * This recreates the session with the same device and installation but gets a new session token.
 *
 * @return A new Context with refreshed session information
 */
fun Context.refreshSession(): Context {
    val serverSession = createSessionServer(
        token = installationToken,
        config = config,
        serverPublicKey = serverPublicKey,
    )

    val sessionTimeoutSeconds = serverSession.getSessionTimeout()
        ?: run {
            logger.warn { "No session timeout found in session server response, using default of 30 minutes" }
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
    val serverPublicKey = installation.ServerPublicKey?.server_public_key ?: error("No server public key")
    val deviceServer = createDeviceServer(installation.Token.token, config, serverPublicKey)
    val serverSession = createSessionServer(installation.Token.token, config, serverPublicKey)

    val sessionTimeoutSeconds: Long = serverSession.getSessionTimeout() ?: run {
        logger.warn { "No session timeout found in session server response, using default of 30 minutes" }
        30 * 60L
    }

    val sessionExpiryTime = sessionTimeoutSeconds.let {
        Instant.now().plusSeconds(it)
    }

    return Context(
        serverPublicKey = serverPublicKey,
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
    val request = CreateInstallation.Request(
        body = body,
    )

    val rawRequest = CreateInstallation.toRawRequest(serialization, request)
    val rawResponse = send(config, rawRequest).requireTyped()
    val res = CreateInstallation.fromRawResponse(serialization, rawResponse)

    when (res) {
        is CreateInstallation.Response200 -> return res.body
        is CreateInstallation.Response400 -> error(setupFailure("create installation", res.body.Error?.firstOrNull()?.error_description))
    }
}

fun createDeviceServer(token: String, config: Config, serverPublicKey: String): DeviceServerCreate {
    val body = DeviceServer(
        description = config.serviceName,
        secret = config.apiKey,
        permitted_ips = listOf("*")
    )
    val request = CreateDeviceServer.Request(
        body = body,
    )

    val rawRequest = CreateDeviceServer.toRawRequest(serialization, request)
    val authRequest = rawRequest.copy(headers = rawRequest.headers + ("X-Bunq-Client-Authentication" to listOf(token)))
    val rawResponse = send(config, authRequest).requireSigned(serverPublicKey)
    val res = CreateDeviceServer.fromRawResponse(serialization, rawResponse)

    when (res) {
        is CreateDeviceServer.Response200 -> return res.body
        is CreateDeviceServer.Response400 -> error(setupFailure("create device server", res.body.Error?.firstOrNull()?.error_description))
    }
}


private fun createSessionServer(
    token: String,
    config: Config,
    serverPublicKey: String,
): SessionServerCreate {
    val body = SessionServer(
        secret = config.apiKey,
    )
    val request = CreateSessionServer.Request(
        body = body,
    )

    val rawRequest = CreateSessionServer.toRawRequest(serialization, request)
    val authRequest = rawRequest.copy(
        headers = rawRequest.headers + ("X-Bunq-Client-Authentication" to listOf(
            token
        ))
    )
    val rawResponse = send(config, authRequest).requireSigned(serverPublicKey)

    val res = CreateSessionServer.fromRawResponse(serialization, rawResponse)

    when (res) {
        is CreateSessionServer.Response200 -> return res.body
        is CreateSessionServer.Response400 -> error(setupFailure("create session server", res.body.Error?.firstOrNull()?.error_description))
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