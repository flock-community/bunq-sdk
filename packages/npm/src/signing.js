"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadRsaKeyPair = loadRsaKeyPair;
exports.signData = signData;
exports.verifyResponse = verifyResponse;
const fs = require("node:fs");
const node_crypto_1 = require("node:crypto");
const privateKeyFile = 'private_key.pem';
const publicKeyFile = 'public_key.pem';
function loadRsaKeyPair() {
    return __awaiter(this, void 0, void 0, function* () {
        let privateKeyPem;
        let publicKeyPem;
        if (fs.existsSync(privateKeyFile) && fs.existsSync(publicKeyFile)) {
            privateKeyPem = fs.readFileSync(privateKeyFile, 'utf-8');
            publicKeyPem = fs.readFileSync(publicKeyFile, 'utf-8');
        }
        else {
            const { privateKey, publicKey } = (0, node_crypto_1.generateKeyPairSync)('rsa', {
                modulusLength: 2048
            });
            privateKeyPem = privateKey.export({
                type: 'pkcs8',
                format: 'pem',
            }).toString();
            publicKeyPem = publicKey.export({
                type: 'spki',
                format: 'pem',
            }).toString();
            fs.writeFileSync(privateKeyFile, privateKeyPem);
            fs.writeFileSync(publicKeyFile, publicKeyPem);
        }
        return [privateKeyPem, publicKeyPem];
    });
}
function signData(data, privateKeyPem) {
    const privateKey = (0, node_crypto_1.createPrivateKey)(privateKeyPem);
    const encodedData = Buffer.from(data, 'utf-8');
    console.log(data);
    console.log(privateKeyPem);
    const signer = (0, node_crypto_1.sign)('SHA256', encodedData, {
        key: privateKey,
        padding: node_crypto_1.constants.RSA_PKCS1_PADDING,
    });
    const encodedSignature = signer.toString('base64');
    return encodedSignature;
}
function verifyResponse(responseBody, signature, serverPublicKeyPem) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const publicKey = (0, node_crypto_1.createPublicKey)(serverPublicKeyPem);
            const decodedSignature = Buffer.from(signature, 'base64');
            const verifier = (0, node_crypto_1.verify)('SHA256', Buffer.from(responseBody, 'utf-8'), {
                key: publicKey,
                padding: node_crypto_1.constants.RSA_PKCS1_PADDING,
            }, decodedSignature);
            return verifier;
        }
        catch (e) {
            console.error(`[ERROR] Signature verification failed: ${e}`);
            return false;
        }
    });
}
