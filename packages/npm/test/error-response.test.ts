import {describe, expect, test} from 'vitest';
import {ReadUser} from "../src/gen/endpoint/ReadUser";
import {failOnNonJsonError, serialization} from "../src/wirespec";

describe('error responses', () => {
    const readUser = (statusCode: number, body: string) =>
        ReadUser.fromRawResponse(serialization, {statusCode, headers: {}, body: new TextEncoder().encode(body)});

    test('a 400 error body without Response envelope is deserialized', () => {
        const response = readUser(400, '{"Error":[{"error_description":"Missing required field \\"currency\\"."}]}');

        expect(response.status).toBe(400);
        expect(response.body).toEqual({Error: [{error_description: 'Missing required field "currency".'}]});
    });

    test('a status other than 200 and 400 is a typed response', () => {
        const response = readUser(403, '{"Error":[{"error_description":"Insufficient authentication."}]}');

        expect(response.status).toBe(403);
        expect(response.body).toEqual({Error: [{error_description: 'Insufficient authentication.'}]});
    });

    test('a body without Response or Error is rejected', () => {
        expect(() => readUser(200, '{"unexpected":true}')).toThrow('neither Response nor Error');
    });

    test('a non-JSON error body names the status', () => {
        const html = {statusCode: 500, headers: {}, body: new TextEncoder().encode('<html>Internal Server Error</html>')};

        expect(() => failOnNonJsonError(html)).toThrow(/500.*<html>/);
    });
});
