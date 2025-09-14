package com.bunq.sdk;

import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

/**
 * Sealed hierarchy for RSA key pairs used in bunq API request signing.
 * 
 * <p>Provides consistent access to both PEM string representations and parsed 
 * RSA key objects, ensuring they remain synchronized.
 * 
 * <p>Available implementations:
 * <ul>
 *   <li>{@link SigningKeysFromPem} - Load from PEM strings (most common)</li>
 *   <li>{@link SigningKeysFromRsa} - Wrap existing RSA key objects</li>
 * </ul>
 * 
 * @since 1.0
 */
sealed interface SigningKeys permits SigningKeysFromPem, SigningKeysFromRsa {
    String publicKeyPem();

    String privateKeyPem();

    RSAPrivateKey privateKey();

    RSAPublicKey publicKey();

}

