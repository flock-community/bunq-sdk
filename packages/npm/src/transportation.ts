import {Wirespec} from "./gen/Wirespec";
import {client} from "./gen/Client";
import {Context, refreshSession} from "./context";
import {rawHandler, serialization} from "./wirespec";

const sessionRejection = "Insufficient authentication.";

function authenticationHeaders({sessionToken, config}: Context): Record<string, string[]> {
    const headers: Record<string, string | undefined> = {
        "X-Bunq-Client-Authentication": sessionToken,
        "Cache-Control": config.cacheControl,
        "X-Bunq-Language": config.language,
        "X-Bunq-Region": config.region,
        "X-Bunq-Client-Request-Id": config.clientRequestId,
        "X-Bunq-Geolocation": config.geolocation,
    };
    return Object.fromEntries(Object.entries(headers).filter(([, value]) => value).map(([key, value]) => [key, [value!]]));
}

// bunq answers a dead session with 403 and this error description; other 403s are real permission errors
function isSessionRejected(response: Wirespec.RawResponse): boolean {
    if (response.statusCode !== 403 || !response.body) return false;
    try {
        const body = JSON.parse(new TextDecoder().decode(response.body));
        return body.Error.some((error: {error_description?: string}) => error.error_description === sessionRejection);
    } catch {
        return false;
    }
}

/**
 * Sends requests with the context's authentication headers.
 * A 403 "Insufficient authentication." refreshes the session once (shared by concurrent requests) and retries the
 * request with the new token. Other responses, and the original 403 when the refresh fails, are returned as is.
 * The refreshed context is kept inside this transportation, so later requests use the new token.
 */
export function transportation(ctx: Context, refresh: (ctx: Context) => Promise<Context> = refreshSession): Wirespec.Transportation {
    let current = ctx;
    let refreshing: Promise<Context | undefined> | undefined;

    const sendWith = (used: Context, request: Wirespec.RawRequest) =>
        rawHandler(used.config, {...request, headers: {...request.headers, ...authenticationHeaders(used)}});

    const refreshed = (used: Context): Promise<Context | undefined> => {
        // another request may have refreshed the session while this one was in flight
        if (current.sessionToken !== used.sessionToken) return Promise.resolve(current);
        refreshing ??= refresh(used)
            .then(fresh => current = fresh)
            .catch(error => {
                console.warn(`bunq session refresh failed: ${error?.message}`);
                return undefined;
            })
            .finally(() => refreshing = undefined);
        return refreshing;
    };

    return {
        async transport(request) {
            const used = current;
            const response = await sendWith(used, request);
            if (!isSessionRejected(response)) return response;
            const fresh = await refreshed(used);
            return fresh ? sendWith(fresh, request) : response;
        }
    };
}

export function bunqClient(ctx: Context) {
    return client(serialization, transportation(ctx));
}
