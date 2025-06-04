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
const vitest_1 = require("vitest");
const context_1 = require("../src/context");
const Openapi_1 = require("../src/Openapi");
const client_1 = require("../src/client");
const serverName = "PeterScript";
const apiKey = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95";
(0, vitest_1.describe)("api test", () => __awaiter(void 0, void 0, void 0, function* () {
    const context = yield (0, context_1.createContext)(apiKey, serverName);
    (0, vitest_1.test)('READ_User', () => __awaiter(void 0, void 0, void 0, function* () {
        var _a;
        const req = Openapi_1.READ_User.request({
            "Cache-Control": undefined,
            "User-Agent": context.serverName,
            "X-Bunq-Client-Authentication": context.sessionToken,
            "X-Bunq-Client-Request-Id": undefined,
            "X-Bunq-Geolocation": undefined,
            "X-Bunq-Language": undefined,
            "X-Bunq-Region": undefined,
            "itemId": context.userId
        });
        const res = yield (0, client_1.client)(context).rEAD_User(req);
        if (res.status === 200) {
            (0, vitest_1.expect)((_a = res.body.UserPerson) === null || _a === void 0 ? void 0 : _a.display_name).toBe("D. Byrne");
        }
        else {
            throw new Error("Cannot read user");
        }
    }));
    (0, vitest_1.test)('list_all_MonetaryAccountBank_for_User', () => __awaiter(void 0, void 0, void 0, function* () {
        const req = Openapi_1.List_all_MonetaryAccountBank_for_User.request({
            "Cache-Control": undefined,
            "User-Agent": context.serverName,
            "X-Bunq-Client-Authentication": context.sessionToken,
            "X-Bunq-Client-Request-Id": undefined,
            "X-Bunq-Geolocation": undefined,
            "X-Bunq-Language": undefined,
            "X-Bunq-Region": undefined,
            "userID": context.userId
        });
        const res = yield (0, client_1.client)(context).list_all_MonetaryAccountBank_for_User(req);
        if (res.status === 200) {
            (0, vitest_1.expect)(res.body[0].display_name).toBe("D. Byrne");
        }
        else {
            throw new Error("Cannot read user");
        }
    }));
}));
