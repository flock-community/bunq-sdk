import {describe, expect, test} from 'vitest'
import {createContext} from "../src/context";
import {rawHandler} from "../src/wirespec";
import {Sdk} from "../src/gen/Sdk";

const serverName = "PeterScript"
const apiKey = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"


describe("api test", async () => {

    const context = await createContext(apiKey, serverName)
    const sdk = Sdk(context, rawHandler)

    test('READ_User', async () => {
        const res = await sdk.rEAD_User({
            "itemId": context.userId
        })
        if(res.status === 200) {
            expect(res.body.UserPerson?.display_name).toBe("D. Byrne")
        } else {
            throw new Error("Cannot read user")
        }
    })

    test('list_all_MonetaryAccountBank_for_User', async () => {
        const res = await sdk.list_all_MonetaryAccountBank_for_User({
            "userID": context.userId
        })
        if(res.status === 200) {
            expect(res.body[0].display_name).toBe("D. Byrne")
        } else {
            throw new Error("Cannot read user")
        }
    })
})
