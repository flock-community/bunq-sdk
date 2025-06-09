import {describe, expect, test} from 'vitest'
import {initContext} from "../src/context";
import {initHandler, rawHandler} from "../src/wirespec";
import {Sdk} from "../src/gen/Sdk";
import {initSigning} from "../src/signing";
import {initConfig} from "../src/config";

const config = initConfig({
    serverName: "PeterScript",
    apiKey: "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95",
    privateKeyFile: "../../private_key.pem",
    publicKeyFile: "../../public_key.pem",
})

describe("api test", async () => {

    const signing = initSigning(config)
    const context = await initContext(config, signing)
    const handler = initHandler(signing, context)
    const sdk = Sdk(handler)

    test('READ_User', async () => {
        const res = await sdk.READ_User({
            "itemId": context.userId
        })
        if(res.status === 200) {
            expect(res.body.UserPerson?.display_name).toBe("D. Byrne")
        } else {
            throw new Error("Cannot read user")
        }
    })

    test('list_all_MonetaryAccountBank_for_User', async () => {
        const res = await sdk.List_all_MonetaryAccountBank_for_User({
            "userID": context.userId
        })
        if(res.status === 200) {
            expect(res.body[0].display_name).toBe("D. Byrne")
        } else {
            throw new Error("Cannot read user")
        }
    })
})
