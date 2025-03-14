import {
    CREATE_DeviceServer,
    CREATE_Installation,
    CREATE_SessionServer,
    READ_User,
    Wirespec
} from "./openapi";
import {loadRsaKeyPair, signData, verifyResponse} from "./signing";
import {Context} from "./context";

type Client =
    CREATE_Installation.Handler &
    CREATE_DeviceServer.Handler &
    CREATE_SessionServer.Handler &
    READ_User.Handler


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
            return JSON.parse(raw) as T;
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

        type Body = {Response: object[]} | {Error: object[]}
        const body:Body = JSON.parse(raw)

        if("Error" in body){
            throw new Error(JSON.stringify(body["Error"]))
        }
        const rawResponse: Wirespec.RawResponse = {
            body: JSON.stringify(body["Response"].reduce((acc,cur) => ({...acc, ...cur}), {})),
            headers: headersIteratorToRecord(res.headers),
            status: res.status
        }


        return client(serialization).from(rawResponse)
    })
};

export const client: (context?:Context) => Client = (context) => ({
    rEAD_User: handleFetch(context, READ_User.client),
    cREATE_Installation: handleFetch(context, CREATE_Installation.client),
    cREATE_DeviceServer: handleFetch(context, CREATE_DeviceServer.client),
    cREATE_SessionServer: handleFetch(context, CREATE_SessionServer.client),
});
