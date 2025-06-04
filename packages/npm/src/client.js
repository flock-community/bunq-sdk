"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.client = void 0;
const Openapi_1 = require("./Openapi");
const signing_1 = require("./signing");
function headersIteratorToRecord(headersIterator) {
    const record = {};
    for (const [key, value] of headersIterator.entries()) {
        record[key] = value;
    }
    return record;
}
const serialization = {
    deserialize(raw) {
        if (raw === undefined) {
            return undefined;
        }
        else {
            const body = JSON.parse(raw);
            if ("Error" in body) {
                throw new Error(JSON.stringify(body["Error"]));
            }
            const response = body["Response"];
            if ("MonetaryAccountBank" in response[0]) {
                return [response[0]["MonetaryAccountBank"]];
            }
            return response.reduce((acc, cur) => (Object.assign(Object.assign({}, acc), cur)), {});
        }
    },
    serialize(type) {
        if (typeof type === "string") {
            return type;
        }
        else {
            return JSON.stringify(type);
        }
    }
};
const handleFetch = (context, client) => (request) => __awaiter(void 0, void 0, void 0, function* () {
    const rawRequest = client(serialization).to(request);
    const url = "https://public-api.sandbox.bunq.com/v1/" + rawRequest.path.join("/");
    const [privateKey, _] = yield (0, signing_1.loadRsaKeyPair)();
    const signatureHeader = rawRequest.body ? { 'X-Bunq-Client-Signature': (0, signing_1.signData)(rawRequest.body, privateKey) } : {};
    const headers = Object.assign(Object.assign({}, rawRequest.headers), signatureHeader);
    if (headers['X-Bunq-Client-Authentication'] === '') {
        delete headers['X-Bunq-Client-Authentication'];
        delete headers['X-Bunq-Client-Signature'];
    }
    if (!headers['X-Bunq-Geolocation'])
        delete headers['X-Bunq-Geolocation'];
    if (!headers['X-Bunq-Region'])
        delete headers['X-Bunq-Region'];
    const options = {
        method: rawRequest.method,
        body: rawRequest.body,
        headers: headers
    };
    return fetch(url, options).then((res) => __awaiter(void 0, void 0, void 0, function* () {
        const raw = yield res.text();
        const serverSignature = res.headers.get('X-Bunq-Server-Signature');
        if (serverSignature && context) {
            if (!(yield (0, signing_1.verifyResponse)(raw, serverSignature, context.serverPublicKey))) {
                throw new Error("Response not verified");
            }
        }
        const rawResponse = {
            body: raw,
            headers: headersIteratorToRecord(res.headers),
            status: res.status
        };
        return client(serialization).from(rawResponse);
    }));
});
const client = (context) => ({
    cREATE_Installation: handleFetch(context, Openapi_1.CREATE_Installation.client),
    cREATE_DeviceServer: handleFetch(context, Openapi_1.CREATE_DeviceServer.client),
    cREATE_SessionServer: handleFetch(context, Openapi_1.CREATE_SessionServer.client),
    rEAD_User: handleFetch(context, Openapi_1.READ_User.client),
    list_all_MonetaryAccountBank_for_User: handleFetch(context, Openapi_1.List_all_MonetaryAccountBank_for_User.client)
});
exports.client = client;
