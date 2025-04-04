import {describe, expect, test} from 'vitest'
import {createContext} from "../src/context";
import {List_all_MonetaryAccountBank_for_User, READ_User} from "../src/Openapi";
import {client} from "../src/client";

const serverName = "PeterScript"
const apiKey = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"


describe("api test", async () => {

    const context = await createContext(apiKey, serverName)

    test('READ_User', async () => {
        const req = READ_User.request({
            "Cache-Control": undefined,
            "User-Agent": context.serverName,
            "X-Bunq-Client-Authentication": context.sessionToken,
            "X-Bunq-Client-Request-Id": undefined,
            "X-Bunq-Geolocation": undefined,
            "X-Bunq-Language": undefined,
            "X-Bunq-Region": undefined,
            "itemId": context.userId
        })
        const res = await client(context).rEAD_User(req)
        if(res.status === 200) {
            expect(res.body.UserPerson?.display_name).toBe("D. Byrne")
        } else {
            throw new Error("Cannot read user")
        }
    })

    test('list_all_MonetaryAccountBank_for_User', async () => {
        const req = List_all_MonetaryAccountBank_for_User.request({
            "Cache-Control": undefined,
            "User-Agent": context.serverName,
            "X-Bunq-Client-Authentication": context.sessionToken,
            "X-Bunq-Client-Request-Id": undefined,
            "X-Bunq-Geolocation": undefined,
            "X-Bunq-Language": undefined,
            "X-Bunq-Region": undefined,
            "userID": context.userId
        })
        const res = await client(context).list_all_MonetaryAccountBank_for_User(req)
        if(res.status === 200) {
            expect(res.body).toBe("D. Byrne")
        } else {
            throw new Error("Cannot read user")
        }
    })
})
