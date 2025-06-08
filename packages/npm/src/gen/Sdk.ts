import { Wirespec } from "./Wirespec"
import {serialization} from "../wirespec";
import {Context} from "../context";

import {READ_User, List_all_MonetaryAccountBank_for_User} from "./endpoint"

type Send = (rawRequest:Wirespec.RawRequest) => Promise<Wirespec.RawResponse>
export const Sdk = (context: Context, send: Send) => ({
    rEAD_User: async (props: {"itemId": number}) => {
        const req = READ_User.request(props)
        const rawReq = READ_User.client(serialization).to(req)
        const authReq: Wirespec.RawRequest = {
            ...rawReq,
            headers: {
                ...rawReq.headers,
                "UserAgent": context.serverName,
                "X-Bunq-Client-Authentication": context.sessionToken,
            }
        }
        const rawRes = await send(authReq)
        return  READ_User.client(serialization).from(rawRes)
    },

    list_all_MonetaryAccountBank_for_User: async (props: {"userID": number}) => {
        const req = List_all_MonetaryAccountBank_for_User.request(props)
        const rawReq = List_all_MonetaryAccountBank_for_User.client(serialization).to(req)
        const authReq: Wirespec.RawRequest = {
            ...rawReq,
            headers: {
                ...rawReq.headers,
                "UserAgent": context.serverName,
                "X-Bunq-Client-Authentication": context.sessionToken,
            }
        }
        const rawRes = await send(authReq)
        return  List_all_MonetaryAccountBank_for_User.client(serialization).from(rawRes)
    },

})