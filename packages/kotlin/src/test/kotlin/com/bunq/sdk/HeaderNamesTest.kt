package com.bunq.sdk

import com.sun.net.httpserver.HttpServer
import community.flock.wirespec.kotlin.Wirespec
import org.junit.jupiter.api.Test
import java.net.InetSocketAddress
import java.time.Instant
import kotlin.test.assertEquals
import kotlin.test.assertNull

class HeaderNamesTest {

    @Test
    fun `header names are sent hyphenated`() {
        val receivedUserAgents = mutableListOf<String?>()
        val receivedCacheControls = mutableListOf<String?>()
        val receivedLegacyUserAgents = mutableListOf<String?>()
        val receivedLegacyCacheControls = mutableListOf<String?>()
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0).apply {
            createContext("/") { exchange ->
                receivedUserAgents += exchange.requestHeaders.getFirst("User-Agent")
                receivedCacheControls += exchange.requestHeaders.getFirst("Cache-Control")
                receivedLegacyUserAgents += exchange.requestHeaders.getFirst("UserAgent")
                receivedLegacyCacheControls += exchange.requestHeaders.getFirst("CacheControl")
                exchange.sendResponseHeaders(200, -1)
                exchange.close()
            }
            start()
        }
        try {
            val config = Config(
                bunqServer = BunqServer("http://127.0.0.1:${server.address.port}/", ""),
                serviceName = "test",
                apiKey = "test",
                signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
                userAgent = "my-agent",
                cacheControl = "no-cache",
            )
            val context = Context(
                serverPublicKey = "",
                deviceId = 1,
                sessionId = 1,
                sessionToken = "token",
                userId = 1,
                sessionExpiryTime = Instant.now(),
                installationToken = "",
                config = config,
            )

            send(config, Wirespec.RawRequest("GET", listOf("ping"), emptyMap(), context.toHeaders(), null))

            assertEquals(listOf<String?>("my-agent"), receivedUserAgents)
            assertEquals(listOf<String?>("no-cache"), receivedCacheControls)
            assertNull(receivedLegacyUserAgents.single())
            assertNull(receivedLegacyCacheControls.single())
        } finally {
            server.stop(0)
        }
    }
}
