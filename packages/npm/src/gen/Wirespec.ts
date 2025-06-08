export namespace Wirespec {
  export type Method = "GET" | "PUT" | "POST" | "DELETE" | "OPTIONS" | "HEAD" | "PATCH" | "TRACE"
  export type RawRequest = { method: Method, path: string[], queries: Record<string, string>, headers: Record<string, string>, body?: string }
  export type RawResponse = { status: number, headers: Record<string, string>, body?: string }
  export type Request<T> = { path: Record<string, unknown>, method: Method, queries?: Record<string, unknown>, headers?: Record<string, unknown>, body?:T }
  export type Response<T> = { status:number, headers?: Record<string, unknown>, body?:T }
  export type Serialization = { serialize: <T>(type: T) => string; deserialize: <T>(raw: string | undefined) => T }
  export type Client<REQ extends Request<unknown>, RES extends Response<unknown>> = (serialization: Serialization) => { to: (request: REQ) => RawRequest; from: (response: RawResponse) => RES }
  export type Server<REQ extends Request<unknown>, RES extends Response<unknown>> = (serialization: Serialization) => { from: (request: RawRequest) => REQ; to: (response: RES) => RawResponse }
  export type Api<REQ extends Request<unknown>, RES extends Response<unknown>> = { name: string; method: Method, path: string, client: Client<REQ, RES>; server: Server<REQ, RES> }
}