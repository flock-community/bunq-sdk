import {Wirespec} from "./gen/Wirespec";
import {client} from "./gen/Client";
import {Context, refreshSession} from "./context";
import {rawHandler, requireTyped, serialization} from "./wirespec";

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

// a session that expires within this many milliseconds is refreshed before the request is sent
const expiryMarginMs = 30_000;

/**
 * Sends requests with the context's authentication headers.
 * A session that has expired (or expires within 30 seconds) is refreshed before the request is sent.
 * A 403 "Insufficient authentication." refreshes the session once (shared by concurrent requests) and retries the
 * request with the new token. Statuses other than 200 and 400, including the original 403 when the refresh fails,
 * are thrown as BunqApiError.
 * The refreshed context is kept inside this transportation, so later requests use the new token.
 * onContextChange is called once with the new context after every successful refresh, so the caller can store it.
 */
export function transportation(
    ctx: Context,
    refresh: (ctx: Context) => Promise<Context> = refreshSession,
    onContextChange: (ctx: Context) => void = () => {},
): Wirespec.Transportation {
    let current = ctx;
    let refreshing: Promise<Context | undefined> | undefined;

    const sendWith = (used: Context, request: Wirespec.RawRequest) =>
        rawHandler(used.config, {...request, headers: {...request.headers, ...authenticationHeaders(used)}});

    const refreshed = (used: Context): Promise<Context | undefined> => {
        // another request may have refreshed the session while this one was in flight
        if (current.sessionToken !== used.sessionToken) return Promise.resolve(current);
        refreshing ??= Promise.resolve().then(() => refresh(used))
            .then(fresh => {
                current = fresh;
                onContextChange(fresh);
                return fresh;
            }, error => {
                console.warn(`bunq session refresh failed: ${error?.message}`);
                return undefined;
            })
            .finally(() => refreshing = undefined);
        return refreshing;
    };

    return {
        async transport(request) {
            const snapshot = current;
            const used = snapshot.sessionExpiryTime.getTime() <= Date.now() + expiryMarginMs ? await refreshed(snapshot) ?? snapshot : snapshot;
            const response = await sendWith(used, request);
            if (!isSessionRejected(response)) return requireTyped(response);
            const fresh = await refreshed(used);
            return requireTyped(fresh ? await sendWith(fresh, request) : response);
        }
    };
}

export function bunqClient(ctx: Context, onContextChange: (ctx: Context) => void = () => {}) {
    return client(serialization, transportation(ctx, refreshSession, onContextChange));
}
