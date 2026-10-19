package com.bunq.sdk

import com.bunq.sdk.generated.endpoint.ListAllMonetaryAccountBankForUser
import community.flock.wirespec.kotlin.Wirespec
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertNull

class PaginationTest {

    private fun list(body: String) = ListAllMonetaryAccountBankForUser.fromRawResponse(
        serialization, Wirespec.RawResponse(200, emptyMap(), body.toByteArray())
    )

    @Test
    fun `a list response keeps the items and the Pagination block`() {
        val response = list(
            """
            {"Response":[{"MonetaryAccountBank":{"id":2,"description":"second"}},{"MonetaryAccountBank":{"id":1,"description":"first"}}],
             "Pagination":{"future_url":"/v1/future?newer_id=2","newer_url":null,"older_url":"/v1/older?older_id=1"}}
            """
        )

        assertIs<ListAllMonetaryAccountBankForUser.Response200>(response)
        assertEquals(listOf(2L, 1L), response.body.Response.map { it.id })
        assertEquals("/v1/future?newer_id=2", response.body.Pagination.future_url)
        assertNull(response.body.Pagination.newer_url)
        assertEquals("/v1/older?older_id=1", response.body.Pagination.older_url)
    }

    @Test
    fun `an empty page has an empty list and its Pagination`() {
        val response = list("""{"Response":[],"Pagination":{"future_url":null,"newer_url":null,"older_url":null}}""")

        assertIs<ListAllMonetaryAccountBankForUser.Response200>(response)
        assertEquals(emptyList(), response.body.Response)
        assertNull(response.body.Pagination.older_url)
    }
}
