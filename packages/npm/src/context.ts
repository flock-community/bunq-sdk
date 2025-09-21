import {DeviceServer, Installation, SessionServer} from "./gen/model";
import {CREATE_DeviceServer, CREATE_Installation, CREATE_SessionServer,} from "./gen/endpoint";
import {rawHandler, serialization} from "./wirespec";
import {Wirespec} from "./gen/Wirespec";
import {Config} from "./config";

export interface Context {
    readonly serverPublicKey: string;
    readonly deviceId: number;
    readonly sessionId: number;
    readonly sessionToken: string;
    readonly userId: number;
    readonly sessionExpiryTime: Date;
    readonly installationToken: string;
    readonly config: Config;
}


export async function initContext(config: Config): Promise<Context> {
    const createInstallation = async () => {
        const body: Installation = {client_public_key: config.signingKeys.publicKeyAsPem()}
        const req = CREATE_Installation.request({body})
        const rawReq = CREATE_Installation.client(serialization).to(req)
        const rawRes = await rawHandler(config, rawReq)
        const res = CREATE_Installation.client(serialization).from(rawRes)
        if (res.status === 200) {
            return res.body
        } else {
            throw new Error("Installation failed")
        }
    }

    const createDeviceServer = async (token: string) => {
        const body: DeviceServer = {
            description: config.serviceName,
            secret: config.apiKey,
            permitted_ips: ["*"]
        }
        const req = CREATE_DeviceServer.request({body})
        const rawReq = CREATE_DeviceServer.client(serialization).to(req)
        const authReq: Wirespec.RawRequest = {
            ...rawReq,
            headers: {
                ...rawReq.headers,
                "X-Bunq-Client-Authentication": token,
            }
        }
        const rawRes = await rawHandler(config, authReq)
        const res = CREATE_DeviceServer.client(serialization).from(rawRes)
        if (res.status === 200) {
            return res.body
        } else {
            throw new Error("Device server creation failed")
        }
    }

    const createSessionServer = async (token: string) => {
        const body: SessionServer = {
            secret: config.apiKey,
        }
        const req = CREATE_SessionServer.request({body})
        const rawReq = CREATE_SessionServer.client(serialization).to(req)
        const authReq: Wirespec.RawRequest = {
            ...rawReq,
            headers: {
                ...rawReq.headers,
                "UserAgent": config.serviceName,
                "X-Bunq-Client-Authentication": token,
            }
        }
        const rawRes = await rawHandler(config, authReq)
        const res = CREATE_SessionServer.client(serialization).from(rawRes)
        if (res.status === 200) {
            return res.body
        } else {
            throw new Error("Session server creation failed")
        }
    }

    const installation = await createInstallation()
    if (!installation.Token?.token) {
        throw new Error("Token not available")
    }
    if (!installation.ServerPublicKey?.server_public_key) {
        throw new Error("No server public key")
    }

    const device = await createDeviceServer(installation.Token.token)
    if (!device.Id?.id) {
        throw new Error("No device id")
    }

    const session = await createSessionServer(installation.Token.token)
    if (!session.Id?.id) {
        throw new Error("No session id")
    }
    if (!session.Token?.token) {
        throw new Error("No session token")
    }

    const userId = getUserId(session);
    const sessionTimeoutSeconds = getSessionTimeout(session);
    const sessionExpiryTime = new Date(Date.now() + sessionTimeoutSeconds * 1000);

    return {
        serverPublicKey: installation.ServerPublicKey.server_public_key,
        deviceId: device.Id.id,
        sessionId: session.Id.id,
        sessionToken: session.Token.token,
        userId,
        sessionExpiryTime,
        installationToken: installation.Token.token,
        config
    }
}

/**
 * Sessions can be for various types of users, of which only one is filled.
 */
function getUserId(session: any): number {
    return session.UserPerson?.id
        ?? session.UserCompany?.id
        ?? session.UserApiKey?.id
        ?? session.UserPaymentServiceProvider?.id
        ?? (() => { throw new Error("No user id found in the SessionServerCreate response"); })();
}

/**
 * Extract session timeout from the user in the SessionServerCreate response.
 */
function getSessionTimeout(session: any): number {
    const timeout = session.UserPerson?.session_timeout
        ?? session.UserCompany?.session_timeout
        ?? session.UserPaymentServiceProvider?.session_timeout
        ?? getUserApiKeySessionTimeout(session.UserApiKey);
        
    if (timeout === undefined) {
        console.log("bunq - No session timeout found in session server response, using default of 30 minutes");
        return 30 * 60; // 30 minutes default
    }
    
    return timeout;
}

function getUserApiKeySessionTimeout(userApiKey: any): number | undefined {
    if (!userApiKey) return undefined;
    
    return getUserApiKeyAnchoredUserSessionTimeout(userApiKey.granted_by_user)
        ?? getUserApiKeyAnchoredUserSessionTimeout(userApiKey.requested_by_user);
}

function getUserApiKeyAnchoredUserSessionTimeout(anchoredUser: any): number | undefined {
    if (!anchoredUser) return undefined;
    
    return anchoredUser.UserPerson?.session_timeout
        ?? anchoredUser.UserCompany?.session_timeout
        ?? anchoredUser.UserPaymentServiceProvider?.session_timeout;
}

/**
 * Refresh this context's session.
 * This recreates the session with the same device and installation but gets a new session token.
 *
 * @param context The existing context to refresh
 * @returns A new Context with refreshed session information
 */
export async function refreshSession(context: Context): Promise<Context> {
    const createSessionServer = async (token: string) => {
        const body: SessionServer = {
            secret: context.config.apiKey,
        }
        const req = CREATE_SessionServer.request({body})
        const rawReq = CREATE_SessionServer.client(serialization).to(req)
        const authReq: Wirespec.RawRequest = {
            ...rawReq,
            headers: {
                ...rawReq.headers,
                "UserAgent": context.config.serviceName,
                "X-Bunq-Client-Authentication": token,
            }
        }
        const rawRes = await rawHandler(context.config, authReq)
        const res = CREATE_SessionServer.client(serialization).from(rawRes)
        if (res.status === 200) {
            return res.body
        } else {
            throw new Error("Session server creation failed")
        }
    }

    const session = await createSessionServer(context.installationToken)
    if (!session.Id?.id) {
        throw new Error("No session id")
    }
    if (!session.Token?.token) {
        throw new Error("No session token")
    }

    const userId = getUserId(session);
    const sessionTimeoutSeconds = getSessionTimeout(session);
    const sessionExpiryTime = new Date(Date.now() + sessionTimeoutSeconds * 1000);

    return {
        serverPublicKey: context.serverPublicKey,
        deviceId: context.deviceId,
        sessionId: session.Id.id,
        sessionToken: session.Token.token,
        userId,
        sessionExpiryTime,
        installationToken: context.installationToken,
        config: context.config
    }
}