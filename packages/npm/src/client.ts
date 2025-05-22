import {
    CREATE_DeviceServer,
    CREATE_Installation,
    CREATE_SessionServer,
    READ_User,
    List_all_MonetaryAccountBank_for_User,
    Wirespec
} from "./Openapi";
import {loadRsaKeyPair, signData, verifyResponse} from "./signing";
import {Context} from "./context";

type Client =
    CREATE_Installation.Handler &
    CREATE_DeviceServer.Handler &
    CREATE_SessionServer.Handler &
    READ_User.Handler &
    List_all_MonetaryAccountBank_for_User.Handler


function headersIteratorToRecord(headersIterator: Headers): Record<string, string> {
    const record: Record<string, string> = {};
    for (const [key, value] of headersIterator.entries()) {
        record[key] = value;
    }
    return record;
}

const serialization: Wirespec.Serialization = {
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

const handleFetch = <Req extends Wirespec.Request<any>, Res extends Wirespec.Response<any>>(context:Context | undefined, client: Wirespec.Client<Req, Res>) => async (request: Req): Promise<Res> => {
    const rawRequest = client(serialization).to(request);
    const url = "https://public-api.sandbox.bunq.com/v1/" + rawRequest.path.join("/")

    const [privateKey, _] = await loadRsaKeyPair()
    const signatureHeader:{'X-Bunq-Client-Signature': string} | {}  = rawRequest.body ? {'X-Bunq-Client-Signature':  signData(rawRequest.body, privateKey)} : {}
    const headers: Record<string, string> = {
        ...rawRequest.headers,
        ...signatureHeader,
    }

    if(headers['X-Bunq-Client-Authentication'] === ''){
        delete headers['X-Bunq-Client-Authentication']
        delete headers['X-Bunq-Client-Signature']
    }

    if(!headers['X-Bunq-Geolocation'])
        delete headers['X-Bunq-Geolocation']

    if(!headers['X-Bunq-Region'])
        delete headers['X-Bunq-Region']

    const options = {
        method: rawRequest.method,
        body: rawRequest.body,
        headers: headers
    }
    return  fetch(url, options).then(async res => {
        const raw = await res.text()

        const serverSignature = res.headers.get('X-Bunq-Server-Signature')
        if(serverSignature && context) {
            if(!await verifyResponse(raw, serverSignature, context.serverPublicKey)){
                throw new Error("Response not verified")
            }
        }

        const rawResponse: Wirespec.RawResponse = {
            body: raw,
            headers: headersIteratorToRecord(res.headers),
            status: res.status
        }

        return client(serialization).from(rawResponse)
    })
};

export const client: (context?:Context) => Client = (context) => ({
    cREATE_Installation: handleFetch(context, CREATE_Installation.client),
    cREATE_DeviceServer: handleFetch(context, CREATE_DeviceServer.client),
    cREATE_SessionServer: handleFetch(context, CREATE_SessionServer.client),
    rEAD_User: handleFetch(context, READ_User.client),
    list_all_MonetaryAccountBank_for_User: handleFetch(context, List_all_MonetaryAccountBank_for_User.client)
});
