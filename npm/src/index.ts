import {READ_User} from "./openapi";
import {client} from "./client";
import {Context, createContext} from "./context";

const readUser = async (contex:Context) => {
    const req = READ_User.request({
        "Cache-Control": undefined,
        "User-Agent": contex.serverName,
        "X-Bunq-Client-Authentication": contex.sessionToken,
        "X-Bunq-Client-Request-Id": undefined,
        "X-Bunq-Geolocation": undefined,
        "X-Bunq-Language": undefined,
        "X-Bunq-Region": undefined,
        itemId: contex.userId
    })
    const res = await client(contex).rEAD_User(req)
    if(res.status === 200) {
        return res.body
    } else {
        throw new Error("Cannot read user")
    }
}

async function main() {
    const serverName = "PeterScript"
    const apiKey = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
    const context = await createContext(apiKey, serverName)
    const user = await readUser(context)
    console.log("Person legal_name", user.UserPerson?.legal_name)
}

main()
