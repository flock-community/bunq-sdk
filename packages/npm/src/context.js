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
exports.createContext = createContext;
const signing_1 = require("./signing");
const Openapi_1 = require("./Openapi");
const client_1 = require("./client");
function createContext(apiKey, serverName) {
    return __awaiter(this, void 0, void 0, function* () {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l;
        const installation = yield createInstallation(serverName);
        if (!((_a = installation.Token) === null || _a === void 0 ? void 0 : _a.token)) {
            throw new Error("No valid token");
        }
        if (!((_b = installation.ServerPublicKey) === null || _b === void 0 ? void 0 : _b.server_public_key)) {
            throw new Error("No valid server public key");
        }
        const device = yield createDeviceServer(serverName, apiKey, installation.Token.token);
        if (!((_c = device.Id) === null || _c === void 0 ? void 0 : _c.id)) {
            throw new Error("Device not found");
        }
        const session = yield createSessionServer(serverName, apiKey, installation.Token.token);
        if (!((_d = session.Id) === null || _d === void 0 ? void 0 : _d.id)) {
            throw new Error("Session id not found");
        }
        if (!((_e = session.Token) === null || _e === void 0 ? void 0 : _e.token)) {
            throw new Error("Session token not found");
        }
        if (!((_f = session.UserPerson) === null || _f === void 0 ? void 0 : _f.id)) {
            throw new Error("Session person not found");
        }
        return {
            apiKey: apiKey,
            serverName: serverName,
            serverPublicKey: (_g = installation.ServerPublicKey) === null || _g === void 0 ? void 0 : _g.server_public_key,
            deviceId: (_h = device.Id) === null || _h === void 0 ? void 0 : _h.id,
            sessionId: (_j = session.Id) === null || _j === void 0 ? void 0 : _j.id,
            sessionToken: (_k = session.Token) === null || _k === void 0 ? void 0 : _k.token,
            userId: (_l = session.UserPerson) === null || _l === void 0 ? void 0 : _l.id
        };
    });
}
const createInstallation = (serverName) => __awaiter(void 0, void 0, void 0, function* () {
    const [_, publicKeyPem] = yield (0, signing_1.loadRsaKeyPair)();
    const body = {
        client_public_key: publicKeyPem
    };
    const req = Openapi_1.CREATE_Installation.request({
        "Cache-Control": undefined,
        "X-Bunq-Client-Request-Id": undefined,
        "X-Bunq-Geolocation": undefined,
        "X-Bunq-Language": undefined,
        "X-Bunq-Region": undefined,
        "X-Bunq-Client-Authentication": "",
        "User-Agent": serverName,
        body
    });
    const res = yield (0, client_1.client)().cREATE_Installation(req);
    if (res.status === 200) {
        return res.body;
    }
    else {
        throw new Error("Installation failed");
    }
});
const createSessionServer = (serverName, apiKey, token) => __awaiter(void 0, void 0, void 0, function* () {
    const body = {
        secret: apiKey,
    };
    const req = Openapi_1.CREATE_SessionServer.request({
        "Cache-Control": undefined,
        "X-Bunq-Client-Request-Id": undefined,
        "X-Bunq-Geolocation": undefined,
        "X-Bunq-Language": undefined,
        "X-Bunq-Region": undefined,
        "X-Bunq-Client-Authentication": token,
        "User-Agent": serverName,
        body
    });
    const res = yield (0, client_1.client)().cREATE_SessionServer(req);
    if (res.status === 200) {
        return res.body;
    }
    else {
        throw new Error("Installation failed");
    }
});
const createDeviceServer = (serverName, apiKey, token) => __awaiter(void 0, void 0, void 0, function* () {
    const body = {
        description: serverName,
        secret: apiKey,
        permitted_ips: ["*"]
    };
    const req = Openapi_1.CREATE_DeviceServer.request({
        "Cache-Control": undefined,
        "X-Bunq-Client-Request-Id": undefined,
        "X-Bunq-Geolocation": undefined,
        "X-Bunq-Language": undefined,
        "X-Bunq-Region": undefined,
        "X-Bunq-Client-Authentication": token,
        "User-Agent": serverName,
        body
    });
    const res = yield (0, client_1.client)().cREATE_DeviceServer(req);
    if (res.status === 200) {
        return res.body;
    }
    else {
        throw new Error("Installation failed");
    }
});
