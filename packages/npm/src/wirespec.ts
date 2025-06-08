import {Wirespec} from "./gen/Wirespec";
import {loadRsaKeyPair, signData, verifyResponse} from "./signing";

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

export const rawHandler: (rawRequest:Wirespec.RawRequest) => Promise<Wirespec.RawResponse> = async (rawRequest) => {
    const url = "https://public-api.sandbox.bunq.com/v1/" + rawRequest.path.join("/")
    const [privateKey, _] = await loadRsaKeyPair()
    const signatureHeader:{'X-Bunq-Client-Signature': string} | {}  = rawRequest.body ? {'X-Bunq-Client-Signature':  signData(rawRequest.body, privateKey)} : {}
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
export const handler = <Req extends Wirespec.Request<any>, Res extends Wirespec.Response<any>>(client: Wirespec.Client<Req, Res>) => async (request: Req): Promise<Res> => {
    const rawRequest = client(serialization).to(request);
    const rawResponse = await rawHandler(rawRequest)
    return client(serialization).from(rawResponse)
};