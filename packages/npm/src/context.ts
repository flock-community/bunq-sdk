import {loadRsaKeyPair} from "./signing";
import {
    DeviceServer,
    Installation,
    SessionServer
} from "./gen/model";
import {
    CREATE_DeviceServer,
    CREATE_Installation,
    CREATE_SessionServer,
} from "./gen/endpoint";
import {rawHandler, serialization} from "./wirespec";
import {Wirespec} from "./gen/Wirespec";

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
    const body: Installation = {client_public_key: publicKeyPem}
    const req = CREATE_Installation.request({body})
    const rawReq = CREATE_Installation.client(serialization).to(req)
    const rawRes = await rawHandler(rawReq)
    const res = CREATE_Installation.client(serialization).from(rawRes)
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
    const req = CREATE_DeviceServer.request({body})
    const rawReq = CREATE_DeviceServer.client(serialization).to(req)
    const authReq: Wirespec.RawRequest = {
        ...rawReq,
        headers:{
            ...rawReq.headers,
            "X-Bunq-Client-Authentication": token,
        }
    }
    const rawRes = await rawHandler(authReq)
    const res = CREATE_DeviceServer.client(serialization).from(rawRes)
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
    const req = CREATE_SessionServer.request({body})
    const rawReq = CREATE_SessionServer.client(serialization).to(req)
    const authReq: Wirespec.RawRequest = {
        ...rawReq,
        headers:{
            ...rawReq.headers,
            "UserAgent": serverName,
            "X-Bunq-Client-Authentication": token,
        }
    }
    const rawRes = await rawHandler(authReq)
    const res = CREATE_SessionServer.client(serialization).from(rawRes)
    if (res.status === 200) {
        return res.body
    } else {
        throw new Error("Installation failed")
    }
}