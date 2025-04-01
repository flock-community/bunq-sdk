package flock.community.bunq_sdk.java;

import java.time.Duration;

public class Config {

    /**
     * Configuration for caching bank-related data.
     *
     * @param balance configuration for caching balance data.
     * @param transactions configuration for caching transaction data.
     */
    public record BankCacheConfig(
            CacheConfig balance,
            CacheConfig transactions
    ) {}

    /**
     * Configuration for setting up a cache.
     *
     * @param enabled indicates if the cache is enabled.
     * @param maxSize the maximum size of the cache, if applicable.
     * @param expireAfterWrite the duration after which the cache entries expire.
     * @param refreshAfterWrite the optional duration after which cache entries are refreshed.
     */
    public record CacheConfig(
            boolean enabled,
            Long maxSize,
            Duration expireAfterWrite,
            Duration refreshAfterWrite
    )
    {
        public CacheConfig {
            if (enabled && expireAfterWrite == null) {
                throw new IllegalArgumentException ("expireAfterWrite cannot be null when cache is enabled");
            }
        }
    }

    /**
     * Configuration for Bunq bank service.
     *
     * @param apiKey the API key used for authentication with the Bunq service.
     * @param bankAccountId the ID of the bank account associated with Bunq services.
     * @param environment the environment setting for Bunq (e.g., PRODUCTION or SANDBOX).
     * @param saveSessionToFile flag indicating whether to save the session to a file.
     */
    public record BankBunqConfig(
            String apiKey,
            Integer bankAccountId,
            BunqEnvironment environment,
            boolean saveSessionToFile
    )
    {}

    /**
     * Enum representing the Bunq environment.
     */
    public enum BunqEnvironment {
        PRODUCTION,
        SANDBOX
    }

    /**
     * Configuration properties for bank-related settings in the application.
     *
     * @param bunq configuration related to Bunq bank services.
     * @param cache configuration for caching bank data like balances and transactions.
     * @param transactionLimit defines the maximum number of transactions to fetch or process.
     */
    public record BankConfig(
            BankBunqConfig bunq,
            BankCacheConfig cache,
            int transactionLimit
    )
    {}
}
