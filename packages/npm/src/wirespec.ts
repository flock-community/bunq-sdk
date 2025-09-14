import {Wirespec} from "./gen/Wirespec";
import {Signing} from "./signing";
import {Context} from "./context";
import {Config} from "./config";

function headersIteratorToRecord(headersIterator: Headers): Record<string, string> {
    const record: Record<string, string> = {};
    for (const [key, value] of headersIterator.entries()) {
        record[key] = value;
    }
    return record;
}

export const serialization: Wirespec.Serialization = {
    deserialize<T>(raw: string | undefined): T {
        if (raw === undefined) {
            return undefined as T;
        } else {
            type Body = {Response: object[]} | {Error: object[]}
            const body:Body = JSON.parse(raw)

            if("Error" in body){
                throw new Error(JSON.stringify(body["Error"]))
            }

            const response = body["Response"]
            if("MonetaryAccountBank" in response[0]) {
                return [response[0]["MonetaryAccountBank"]] as T;
            }
            return response.reduce((acc,cur) => ({...acc, ...cur}), {}) as T;
        }
    },
    serialize<T>(type: T): string {
        if (typeof type === "string") {
            return type;
        } else {
            return JSON.stringify(type);
        }
    }
};

export const rawHandler: (config: Config, rawRequest:Wirespec.RawRequest) => Promise<Wirespec.RawResponse> = async (config, rawRequest) => {
    const url = config.bunqServer.baseUrl + rawRequest.path.join("/")
    const signatureHeader:{'X-Bunq-Client-Signature': string} | {}  = rawRequest.body ? {'X-Bunq-Client-Signature':  Signing.signData(config, rawRequest.body)} : {}
    const headers: Record<string, string> = {
        ...rawRequest.headers,
        ...signatureHeader,
    }
    const options = {
        method: rawRequest.method,
        body: rawRequest.body,
        headers: headers
    }
    return  fetch(url, options).then(async res => {
        const raw = await res.text()

        const serverSignature = res.headers.get('X-Bunq-Server-Signature')
        // if(serverSignature && context) {
        //     if(!await verifyResponse(raw, serverSignature, context.serverPublicKey)){
        //         throw new Error("Response not verified")
        //     }
        // }

        const rawResponse: Wirespec.RawResponse = {
            body: raw,
            headers: headersIteratorToRecord(res.headers),
            status: res.status
        }

        return rawResponse
    })
}

type Handler = <REQ extends Wirespec.Request<unknown>, RES extends Wirespec.Response<unknown>> (client: Wirespec.Client<REQ, RES>, req:REQ) => Promise<RES>
export const initHandler: (context: Context) => Handler = (context) => async (client, req) => {
    const rawReq = client(serialization).to(req)
    const authReq: Wirespec.RawRequest = {
        ...rawReq,
        headers: {
            ...rawReq.headers,
            "UserAgent": context.config.serviceName,
            "X-Bunq-Client-Authentication": context.sessionToken,
            ...(context.config.userAgent && { "UserAgent": context.config.userAgent }),
            ...(context.config.cacheControl && { "Cache-Control": context.config.cacheControl }),
            ...(context.config.language && { "X-Bunq-Language": context.config.language }),
            ...(context.config.region && { "X-Bunq-Region": context.config.region }),
            ...(context.config.clientRequestId && { "X-Bunq-Client-Request-Id": context.config.clientRequestId }),
            ...(context.config.geolocation && { "X-Bunq-Geolocation": context.config.geolocation }),
        }
    }
    const rawRes = await rawHandler(context.config, authReq)
    return client(serialization).from(rawRes)
};