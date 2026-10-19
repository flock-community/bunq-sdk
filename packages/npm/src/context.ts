import {DeviceServer, Installation, SessionServer} from "./gen/model";
import {client} from "./gen/Client";
import {rawHandler, requireSigned, requireTyped, serialization} from "./wirespec";
import {Config, describeConfig} from "./config";

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


/**
 * String form of a Context with sessionToken, installationToken and the config secrets masked.
 * Logging the object itself or JSON.stringify(context) prints the secrets; the object still holds them.
 */
export function describeContext(context: Context): string {
    return `Context ${JSON.stringify({
        serverPublicKey: context.serverPublicKey, deviceId: context.deviceId, sessionId: context.sessionId,
        sessionToken: '***', userId: context.userId, sessionExpiryTime: context.sessionExpiryTime,
        installationToken: '***', config: '<config>',
    })} ${describeConfig(context.config)}`;
}

function setupFailure(what: string, body: {Error?: {error_description?: string}[]}): string {
    return `${what} (status 400): ${body.Error?.[0]?.error_description}`;
}

// serverPublicKey is not known yet for the installation call, so that response is not verified
function unauthenticatedClient(config: Config, token?: string, serverPublicKey?: string) {
    const headers: Record<string, string[]> = token ? {"X-Bunq-Client-Authentication": [token]} : {};
    return client(serialization, {transport: async request => {
        const response = await rawHandler(config, {...request, headers: {...request.headers, ...headers}});
        return serverPublicKey ? requireSigned(response, serverPublicKey) : requireTyped(response);
    }});
}

export async function initContext(config: Config): Promise<Context> {
    const createInstallation = async () => {
        const body: Installation = {client_public_key: config.signingKeys.publicKeyAsPem()}
        const res = await unauthenticatedClient(config).createInstallation({body})
        if (res.status === 200) {
            return res.body
        } else {
            throw new Error(setupFailure("Installation failed", res.body))
        }
    }

    const createDeviceServer = async (token: string, serverPublicKey: string) => {
        const body: DeviceServer = {
            description: config.serviceName,
            secret: config.apiKey,
            permitted_ips: ["*"]
        }
        const res = await unauthenticatedClient(config, token, serverPublicKey).createDeviceServer({body})
        if (res.status === 200) {
            return res.body
        } else {
            throw new Error(setupFailure("Device server creation failed", res.body))
        }
    }

    const createSessionServer = async (token: string, serverPublicKey: string) => {
        const body: SessionServer = {
            secret: config.apiKey,
        }
        const res = await unauthenticatedClient(config, token, serverPublicKey).createSessionServer({body})
        if (res.status === 200) {
            return res.body
        } else {
            throw new Error(setupFailure("Session server creation failed", res.body))
        }
    }

    const installation = await createInstallation()
    if (!installation.Token?.token) {
        throw new Error("Token not available")
    }
    if (!installation.ServerPublicKey?.server_public_key) {
        throw new Error("No server public key")
    }

    const device = await createDeviceServer(installation.Token.token, installation.ServerPublicKey.server_public_key)
    if (!device.Id?.id) {
        throw new Error("No device id")
    }

    const session = await createSessionServer(installation.Token.token, installation.ServerPublicKey.server_public_key)
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
        const res = await unauthenticatedClient(context.config, token, context.serverPublicKey).createSessionServer({body})
        if (res.status === 200) {
            return res.body
        } else {
            throw new Error(setupFailure("Session server creation failed", res.body))
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