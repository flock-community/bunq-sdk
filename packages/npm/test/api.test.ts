import {describe, expect, test} from 'vitest';
import {Context, initContext, refreshSession} from "../src/context";
import {client as generatedClient} from "../src/gen/Client";
import {rawHandler, requireTyped, serialization} from "../src/wirespec";
import {bunqClient, transportation} from "../src/transportation";
import {createConfig} from "../src/config";
import {BUNQ_SANDBOX_SERVER} from "../src/bunq-server";

// For testing, we'll use the same keys from the test files
const PRIVATE_KEY_PEM = `-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCc03+2+6elFBvL
o2/kml0JylB3smHXfk0HJK02hL0FxMY6JRFWnTqrUyMI7zi4KvuA06DsXhacH0ZZ
kGN4SarJ0NwFi8NK40ZpkyTYgzs80OqhzONnKtpfEZtgEKOnEodFx2xnp0DzLVWt
FvnpDcP8dQ65klmG6tDmnn3ZyPLQy4YOJvemSaU3E1i1Aj0b+jXbyj/XYLvc83E8
/4FlR183ugaDRpTN/NwU7Z5Sj/8ryI4Jf3aYiVOIP+m0aYJzvPJ8ACC2be4XNbBK
SzmdePFRaaYJAHR2GDaPa15k5xQkMzyH9Cg2eXpO1lnOY5vlYUZBCMtYQxpUff5I
dZRh4VStAgMBAAECggEAGL9IRVIHZaWbcEJJbyfLvDaEharsxSJdWd34BmUiZeVk
CXtddc9IWY48NlX3m5pOx0i9+WashzTpN0txYuMvE/tFKQvhxLDCJPlPBGqK/8EQ
8XjhPp+0x3FCFUHy7TOfjIuYZ+/s8CLMhQyd4aCmN3GqYe69+WwXDHlgrywGYxun
SPdyk2WYhYp/3yLdN8fELM2kJPuHI5Bu25dkSc/fhaUVDgdKX84/SByhKfzq0zya
3WbrPGhyoQytey5GLxi0Q4UGHBkNEMYDdVMYorEnzfZOksy3Dp+n4xvu6793cLBU
C987jknCSb3IFjys3MTPwNdA1+f8SfmhQOcSPTclIQKBgQDZUBYBKmzAh2v8uh94
EtnTJS1LAItwgWrqCwwsbOrydhU9KHCIpzHZVbsFcHOjOFPZVYi6XnVQbacJAGDx
CqWH6+h8WMMJVxybsVAPsjKkRfbT/KZrgcYFDP4qISMEXp6v+BrMbi/XIEiB4tWT
1YJiqm7TdgIDeV7A1NtNoIf2oQKBgQC4vsQYJaDBYi3mTVxEHPLdMc5cTUIlr5JL
phDEdqVatD/KlWbcZ6IYqfLRW03zy2r/8VQGCp7B7ssj2iE585fRohNB5C7j8BaA
E9DBQHoa4+BeW461e0mCuiI/irhK58Pfeg1rBJlnyNgfRe51Vw2Bqev64zFlhnWF
T8zewBO+jQKBgQCCqLBSSxvQNpwq/A1nuI3XcgbljZJJNsb9qV7MZ0BsP6tNdj8T
KtPCBNXJ027zuC5SAiePRrPqg8Nmmh+vTeNw8dp6yTObLhE5W0bz6QSh2J8rnkDB
aumQp9s5oWrYebuXuekC+U0yX2q5DZW0qS8X+7le0xkq1ZKvBkxFRDv7gQKBgBGZ
Qo7WTsj9NEgjCG4In+4IR5MtXObAIdyI9kHw13GbiBQhRUorqRpWXiYpX3Sg5RF6
iLmGm3b362v/5HhjxwuWN+Vn+juGbG5I9PLj1H3pRT9X03FgTDFiz85jxYiFKXiJ
ZOvT5VUoocXg4IVXBJdce3lL2THFrD5FystRWtAlAoGABTdVLZ4iHuEHClRMgxXM
+kJ1iRyz54nDySJI7922TYt9LmMOWhWqijAuLbbbZ7PAsxtO6TCqUdSsy+Jx2Y2G
PO/olJBKnIN3f0MpCBz5oFBMkfNsbQ4bPVD2V3pwcdf2HLydTwk49o6WZFar/FGG
os8c7u7MfsR3Tl/MGtJGsH0=
-----END PRIVATE KEY-----`;

const PUBLIC_KEY_PEM = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnNN/tvunpRQby6Nv5Jpd
CcpQd7Jh135NByStNoS9BcTGOiURVp06q1MjCO84uCr7gNOg7F4WnB9GWZBjeEmq
ydDcBYvDSuNGaZMk2IM7PNDqoczjZyraXxGbYBCjpxKHRcdsZ6dA8y1VrRb56Q3D
/HUOuZJZhurQ5p592cjy0MuGDib3pkmlNxNYtQI9G/o128o/12C73PNxPP+BZUdf
N7oGg0aUzfzcFO2eUo//K8iOCX92mIlTiD/ptGmCc7zyfAAgtm3uFzWwSks5nXjx
UWmmCQB0dhg2j2teZOcUJDM8h/QoNnl6TtZZzmOb5WFGQQjLWEMaVH3+SHWUYeFU
rQIDAQAB
-----END PUBLIC KEY-----`;

const config = createConfig(
    BUNQ_SANDBOX_SERVER,
    "PeterScript",
    "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95",
    PRIVATE_KEY_PEM,
    PUBLIC_KEY_PEM
);

describe("API test", async () => {
    const context = await initContext(config);
    const client = bunqClient(context);

    test('readUser should return Donald Byrne', async () => {
        const res = await client.readUser({
            "itemId": context.userId
        });
        
        if (res.status === 200) {
            expect(res.body.UserPerson?.legal_name).toBe("Donald Byrne");
        } else {
            throw new Error("Cannot read user");
        }
    });

    test('listAllMonetaryAccountBankForUser should return D. Byrne account', async () => {
        const res = await client.listAllMonetaryAccountBankForUser({
            "userID": context.userId,
            count: undefined,
            newer_id: undefined,
            older_id: undefined,
        });
        
        if (res.status === 200) {
            expect(res.body[0].display_name).toBe("D. Byrne");
            expect(res.body).toHaveLength(1);
        } else {
            throw new Error("Cannot list monetary accounts");
        }
    });

    test('account should have positive balance', async () => {
        const res = await client.listAllMonetaryAccountBankForUser({
            "userID": context.userId,
            count: undefined,
            newer_id: undefined,
            older_id: undefined,
        });
        
        if (res.status === 200) {
            const account = res.body[0];
            const balance = parseFloat(account.balance?.value || "0");
            expect(balance).toBeGreaterThan(0);
            expect(account.balance?.currency).toBe("EUR");
        } else {
            throw new Error("Cannot list monetary accounts");
        }
    });

    test('refresh session should create refreshed session context', async () => {
        // Refresh the session
        const refreshedContext = await refreshSession(context);
        
        // Verify the context maintains correct data
        expect(refreshedContext.userId).toBe(context.userId); // Same user
        expect(refreshedContext.deviceId).toBe(context.deviceId); // Same device
        expect(refreshedContext.serverPublicKey).toBe(context.serverPublicKey); // Same server key
        expect(refreshedContext.installationToken).toBe(context.installationToken); // Same installation token
        expect(refreshedContext.config).toBe(context.config); // Same config
        
        // Verify session expiry time was updated (should be newer)
        expect(refreshedContext.sessionExpiryTime.getTime()).toBeGreaterThanOrEqual(context.sessionExpiryTime.getTime());
        
        // Verify session token and ID are present (bunq may reuse tokens in sandbox)
        expect(refreshedContext.sessionToken).toBeTruthy();
        expect(refreshedContext.sessionId).toBeTruthy();
        expect(typeof refreshedContext.sessionToken).toBe('string');
        expect(typeof refreshedContext.sessionId).toBe('number');
        
        // The refreshed context should be able to create a valid client
        expect(() => bunqClient(refreshedContext)).not.toThrow();
    });
});

describe("dead session", () => {
    test('a deleted session is refreshed once and the call succeeds', async () => {
        // no session and no server public key exist yet, so this one call is not signature-verified
        const unauthenticated = generatedClient(serialization, {transport: async request => requireTyped(await rawHandler(config, request))});
        const sandboxUser = await unauthenticated.createSandboxUserPerson({body: {}});
        if (sandboxUser.status !== 200 || !sandboxUser.body.ApiKey?.api_key) {
            throw new Error("Cannot create sandbox user");
        }
        const sandboxConfig = createConfig(BUNQ_SANDBOX_SERVER, "PeterScript", sandboxUser.body.ApiKey.api_key, PRIVATE_KEY_PEM, PUBLIC_KEY_PEM);
        const context = await initContext(sandboxConfig);
        let refreshes = 0;
        const client = generatedClient(serialization, transportation(context, async ctx => { refreshes++; return refreshSession(ctx); }));

        expect((await client.listAllMonetaryAccountBankForUser({userID: context.userId})).status).toBe(200);
        expect(refreshes).toBe(0);

        expect((await client.deleteSession({itemId: context.sessionId})).status).toBe(200);

        expect((await client.listAllMonetaryAccountBankForUser({userID: context.userId})).status).toBe(200);
        expect(refreshes).toBe(1);
    }, 30_000); // about eight sequential sandbox calls; from CI runners this can exceed the 5 s default
});
