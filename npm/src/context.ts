import {loadRsaKeyPair} from "./signing";
import {
    CREATE_DeviceServer,
    CREATE_Installation,
    CREATE_SessionServer,
    DeviceServer,
    Installation,
    SessionServer
} from "./Openapi";
import {client} from "./client";


export type Context = {
    apiKey:string,
    serverName:string,
    serverPublicKey:string,
    deviceId: number
    sessionId: number
    sessionToken: string
    userId: number
}


export async function createContext (apiKey:string, serverName:string):Promise<Context> {
    const installation = await createInstallation(serverName)
    if (!installation.Token?.token) {throw new Error("No valid token")}
    if (!installation.ServerPublicKey?.server_public_key) {throw new Error("No valid server public key")}

    const device = await createDeviceServer(serverName, apiKey, installation.Token.token)
    if(!device.Id?.id){throw new Error("Device not found")}

    const session = await createSessionServer(serverName, apiKey, installation.Token.token)
    if(!session.Id?.id){throw new Error("Session id not found")}
    if(!session.Token?.token){throw new Error("Session token not found")}
    if(!session.UserPerson?.id){throw new Error("Session person not found")}

    return  {
        apiKey: apiKey,
        serverName: serverName,
        serverPublicKey: installation.ServerPublicKey?.server_public_key,
        deviceId: device.Id?.id,
        sessionId: session.Id?.id,
        sessionToken: session.Token?.token,
        userId: session.UserPerson?.id
    }
}

const createInstallation = async (serverName: string,) => {
    const [_, publicKeyPem] = await loadRsaKeyPair()
    const body: Installation = {
        client_public_key: publicKeyPem
    }
    const req = CREATE_Installation.request({
        "Cache-Control": undefined,
        "X-Bunq-Client-Request-Id": undefined,
        "X-Bunq-Geolocation": undefined,
        "X-Bunq-Language": undefined,
        "X-Bunq-Region": undefined,
        "X-Bunq-Client-Authentication": "",
        "User-Agent": serverName,
        body
    })
    const res = await client().cREATE_Installation(req)
    if (res.status === 200) {
        return res.body
    } else {
        throw new Error("Installation failed")
    }
}

const createSessionServer = async (serverName: string, apiKey: string, token: string) => {
    const body: SessionServer = {
        secret: apiKey,
    }
    const req = CREATE_SessionServer.request({
        "Cache-Control": undefined,
        "X-Bunq-Client-Request-Id": undefined,
        "X-Bunq-Geolocation": undefined,
        "X-Bunq-Language": undefined,
        "X-Bunq-Region": undefined,
        "X-Bunq-Client-Authentication": token,
        "User-Agent": serverName,
        body
    })
    const res = await client().cREATE_SessionServer(req)
    if (res.status === 200) {
        return res.body
    } else {
        throw new Error("Installation failed")
    }
}

const createDeviceServer = async (serverName: string, apiKey: string, token: string) => {
    const body: DeviceServer = {
        description: serverName,
        secret: apiKey,
        permitted_ips: ["*"]
    }
    const req = CREATE_DeviceServer.request({
        "Cache-Control": undefined,
        "X-Bunq-Client-Request-Id": undefined,
        "X-Bunq-Geolocation": undefined,
        "X-Bunq-Language": undefined,
        "X-Bunq-Region": undefined,
        "X-Bunq-Client-Authentication": token,
        "User-Agent": serverName,
        body
    })
    const res = await client().cREATE_DeviceServer(req)
    if (res.status === 200) {
        return res.body
    } else {
        throw new Error("Installation failed")
    }
}