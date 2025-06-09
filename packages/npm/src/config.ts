export type Config = {
    serverName:string,
    apiKey:string,
    privateKeyFile:string,
    publicKeyFile:string,
    userAgent?: string
    cacheControl?: string
    region?: string
    clientRequestId?: string
    geolocation?: string
}

export const initConfig: (config: Config) => Config = (config) => ({
    ...config,
    privateKeyFile: config.privateKeyFile ?? 'private_key.pem',
    publicKeyFile: config.publicKeyFile ?? 'public_key.pem',
})