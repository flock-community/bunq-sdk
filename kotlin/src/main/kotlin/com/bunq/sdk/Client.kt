package com.bunq.sdk

import com.bunq.sdk.generated.List_all_MonetaryAccountBank_for_UserEndpoint
import com.bunq.sdk.generated.READ_UserEndpoint
import community.flock.wirespec.kotlin.Wirespec
import kotlin.reflect.full.companionObjectInstance


class Client(private val signing: Signing, private val context: Context): List_all_MonetaryAccountBank_for_UserEndpoint.Handler, READ_UserEndpoint.Handler {
    override suspend fun list_all_MonetaryAccountBank_for_User(request: List_all_MonetaryAccountBank_for_UserEndpoint.Request): List_all_MonetaryAccountBank_for_UserEndpoint.Response<*> = handle(signing, context, request)
    override suspend fun rEAD_User(request: READ_UserEndpoint.Request): READ_UserEndpoint.Response<*> = handle(signing, context, request)
}

fun <Req: Wirespec.Request<*>, Res:Wirespec.Response<*> >handle(signing: Signing, context: Context, request:Req): Res{
    val declaringClass = request::class.java.declaringClass
    val handler = declaringClass.declaredClasses.toList().find { it.simpleName == "Handler" } ?: error("Handler not found")
    val instance = handler.kotlin.companionObjectInstance as Wirespec.Client<Wirespec.Request<*>, Wirespec.Response<*>>
    val client = instance.client(serialization)
    val rawRequest = client.to(request as Wirespec.Request<*>)
    val reqToken = rawRequest.copy(headers = rawRequest.headers + ("X-Bunq-Client-Authentication" to listOf(context.sessionToken)))
    val rawResponse = send(signing, reqToken)
    return client.from(rawResponse) as Res
}