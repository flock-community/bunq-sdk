package com.bunq.sdk

import com.sun.net.httpserver.HttpServer
import community.flock.wirespec.kotlin.Wirespec
import java.net.InetSocketAddress
import java.net.http.HttpTimeoutException
import java.time.Duration
import java.util.Optional
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertNull

class SendTest {

    private fun config(port: Int, connectTimeout: Duration? = null, requestTimeout: Duration? = null) = Config(
        bunqServer = BunqServer("http://127.0.0.1:$port/", ""),
        serviceName = "test",
        apiKey = "key",
        signingKeys = BunqSigningKeysGenerator.generateBunqSigningKeys(),
        connectTimeout = connectTimeout,
        requestTimeout = requestTimeout,
    )

    private fun receivedQuery(queries: Map<String, List<String>>): String? {
        var query: String? = null
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0).apply {
            createContext("/") { exchange ->
                query = exchange.requestURI.rawQuery
                exchange.sendResponseHeaders(200, -1)
                exchange.close()
            }
            start()
        }
        try {
            send(config(server.address.port), Wirespec.RawRequest("GET", listOf("payment"), queries, emptyMap(), null))
        } finally {
            server.stop(0)
        }
        return query
    }

    @Test
    fun `query parameters without a value are left out`() {
        val query = receivedQuery(mapOf("count" to listOf("200"), "newer_id" to emptyList(), "older_id" to emptyList()))

        assertEquals("count=200", query)
    }

    @Test
    fun `no query string is sent when no parameter has a value`() {
        assertNull(receivedQuery(mapOf("newer_id" to emptyList(), "older_id" to emptyList())))
    }

    @Test
    fun `a request without an answer within the request timeout throws HttpTimeoutException`() {
        val release = CountDownLatch(1)
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0).apply {
            createContext("/") { exchange ->
                release.await(10, TimeUnit.SECONDS)
                exchange.close()
            }
            start()
        }
        try {
            val config = config(server.address.port, requestTimeout = Duration.ofMillis(200))

            assertFailsWith<HttpTimeoutException> {
                send(config, Wirespec.RawRequest("GET", listOf("ping"), emptyMap(), emptyMap(), null))
            }
        } finally {
            release.countDown()
            server.stop(0)
        }
    }

    @Test
    fun `the connect timeout is set on the HTTP client`() {
        val timeout = Duration.ofSeconds(3)

        assertEquals(Optional.of(timeout), httpClientFor(config(1, connectTimeout = timeout)).connectTimeout())
        assertEquals(Optional.empty(), httpClientFor(config(1)).connectTimeout())
    }
}
