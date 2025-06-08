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

export const config: (config: Config) => Config = (config) => ({
    ...config
})