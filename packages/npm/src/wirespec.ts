import {Wirespec} from "./gen/Wirespec";
import {Signing} from "./signing";
import {Config} from "./config";

const utf8Decoder = new TextDecoder();
const utf8Encoder = new TextEncoder();

const arrayType = "[]";

function singleValue<T>(values: string[], type: string): T {
    switch (type) {
        case "number": return Number(values[0]) as T;
        case "boolean": return (values[0] === "true") as T;
        default: return values[0] as T;
    }
}

export const serialization: Wirespec.Serialization = {
    serializeBody<T>(t: T): Uint8Array {
        return utf8Encoder.encode(typeof t === "string" ? t : JSON.stringify(t));
    },
    deserializeBody<T>(raw: Uint8Array, type: string): T {
        const body: {Response?: Record<string, unknown>[]} = JSON.parse(utf8Decoder.decode(raw));
        // error responses have no Response envelope and are typed as such by the generated client
        if (!body.Response) {
            return body as T;
        }
        if (type.endsWith(arrayType)) {
            return body.Response.flatMap(item => Object.values(item)) as T;
        }
        return body.Response.reduce((acc, cur) => ({...acc, ...cur}), {}) as T;
    },
    serializePath<T>(t: T): string {
        return String(t);
    },
    deserializePath<T>(raw: string, type: string): T {
        return singleValue([raw], type);
    },
    serializeParam<T>(value: T): string[] {
        return Array.isArray(value) ? value.map(String) : [String(value)];
    },
    deserializeParam<T>(values: string[], type: string): T {
        return (type.endsWith(arrayType)
            ? values.map(value => singleValue([value], type.slice(0, -arrayType.length)))
            : singleValue(values, type)) as T;
    },
};

export const rawHandler: (config: Config, rawRequest: Wirespec.RawRequest) => Promise<Wirespec.RawResponse> = async (config, rawRequest) => {
    const url = new URL(config.bunqServer.baseUrl + rawRequest.path.join("/"));
    Object.entries(rawRequest.queries).forEach(([key, values]) => values.forEach(value => url.searchParams.append(key, value)));

    const headers = new Headers({"User-Agent": config.userAgent?.trim() || config.serviceName});
    Object.entries(rawRequest.headers).forEach(([key, values]) => values.forEach(value => value.trim() && headers.append(key, value)));
    if (rawRequest.body) {
        headers.set("X-Bunq-Client-Signature", Signing.signData(config, utf8Decoder.decode(rawRequest.body)));
    }

    const res = await fetch(url, {method: rawRequest.method, body: rawRequest.body, headers});
    const body = new Uint8Array(await res.arrayBuffer());

    const responseHeaders: Record<string, string[]> = {};
    res.headers.forEach((value, key) => responseHeaders[key] = [value]);
    return {statusCode: res.status, headers: responseHeaders, body: body.length ? body : undefined};
}
