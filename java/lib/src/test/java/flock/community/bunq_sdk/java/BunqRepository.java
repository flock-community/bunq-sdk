package flock.community.bunq_sdk.java;

import com.bunq.sdk.context.ApiContext;
import com.bunq.sdk.context.ApiEnvironmentType;
import com.bunq.sdk.context.BunqContext;
import com.bunq.sdk.exception.ApiException;
import com.bunq.sdk.exception.BunqException;
import com.bunq.sdk.http.Pagination;
import com.bunq.sdk.model.generated.endpoint.MonetaryAccountBank;
import com.bunq.sdk.model.generated.endpoint.Payment;
import flock.community.bunq_sdk.java.Config.BunqEnvironment;
//import jakarta.annotation.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

import static com.bunq.sdk.context.ApiEnvironmentType.PRODUCTION;
import static com.bunq.sdk.context.ApiEnvironmentType.SANDBOX;
import static com.bunq.sdk.context.BunqContext.loadApiContext;
import static flock.community.bunq_sdk.java.BunqSandboxRepositoryHelper.createSandboxApiContext;
import static flock.community.bunq_sdk.java.BunqSandboxRepositoryHelper.requestSpendingMoneyIfNeeded;

/**
 * This repository translates teambalance's domain into bunq domain, and performs requests to Bunq through its Java SDK.
 * <p>
 * Copy/pasted and adapted from <a href="https://github.com/bunq/tinker_java">Bunq's tinker project </a>
 */
public class BunqRepository {
    private static final Logger log = LoggerFactory.getLogger(BunqRepository.class);

    /**
     * FileName constants.
     */
    private static final String FILE_NAME_BUNQ_CONF_PRODUCTION = "bunq-production.conf";
    private static final String FILE_NAME_BUNQ_CONF_SANDBOX = "bunq-sandbox.conf";

    /**
     * Concurrency constants
     */

    private static final Duration acquireMaxWaitDuration = Duration.ofSeconds(5);
    /**
     * A semaphore is used to limit the amount of open calls to Bunq to 1.
     */
    private static final Semaphore semaphore = new Semaphore(1);
    private final Map<Integer, Integer> accountIdsToValidatedAccountIds = new HashMap<>();
    private final ApiEnvironmentType environmentType;
    private final String apiKey;
    private final Boolean saveSessionToFile;

    public BunqRepository(ApiEnvironmentType environmentType,
                          String apiKey,
                          Boolean saveSessionToFile) throws UnknownHostException {
        if (PRODUCTION == environmentType && apiKey == null) {
            throw new IllegalArgumentException("Apikey is expected for production environment");
        }
        log.info("Starting BunqRepository of type {}", environmentType);

        this.environmentType = environmentType;
        this.apiKey = apiKey;
        this.saveSessionToFile = saveSessionToFile;

        setupContext();
    }

    public BunqRepository(Config.BankBunqConfig config) throws UnknownHostException {
        this(
                toApiEnvironmentType(config.environment()),
                config.apiKey(),
                config.saveSessionToFile()
        );
    }

    public Integer checkAccountId(Integer accountId) {
        return accountIdsToValidatedAccountIds.computeIfAbsent(accountId, x -> {
            if (environmentType == PRODUCTION) {
                return validateAccountId(accountId);
            } else {
                return getAccountId();
            }
        });
    }

    private int getAccountId() {
        Pagination pagination = new Pagination();
        pagination.setCount(100);

        List<MonetaryAccountBank> allAccount = MonetaryAccountBank.list(pagination.getUrlParamsCountOnly()).getValue();

        return allAccount.stream()
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("There are no active accounts enabled for the current user / session"))
                .getId();
    }

    private int validateAccountId(Integer accountId) {
        Pagination pagination = new Pagination();
        pagination.setCount(100);

        List<MonetaryAccountBank> allAccount = MonetaryAccountBank.list(pagination.getUrlParamsCountOnly()).getValue();

        return allAccount.stream()
                .filter(monetaryAccountBank -> accountId.equals(monetaryAccountBank.getId()))
                .findFirst().orElseThrow(() -> {
                    final String error = ("""
                            There is no account with id %s present \
                            and/or enabled for access with the current API key \
                            """).formatted(accountId);
                    log.error(error);
                    return new IllegalStateException(error);
                }).getId();
    }

    private static ApiEnvironmentType toApiEnvironmentType(BunqEnvironment environment) {
        return switch (environment) {
            case PRODUCTION -> PRODUCTION;
            case SANDBOX -> SANDBOX;
        };
    }

    public MonetaryAccountBank getMonetaryAccountBank(int accountId) {
        return withSemaphore(() -> {
            var validatedAccountId = checkAccountId(accountId);
            return MonetaryAccountBank.get(validatedAccountId).getValue();
        });
    }

    public List<Payment> getAllPayments(int accountId, int count) {
        return withSemaphore(() -> {
            Pagination pagination = new Pagination();
            pagination.setCount(count);
            var validatedAccountId = checkAccountId(accountId);
            return Payment.list(
                    validatedAccountId,
                    pagination.getUrlParamsCountOnly()
            ).getValue();

        });
    }

    public void updateContext() {
        safeSave(BunqContext.getApiContext());
    }

    private <T> T withSemaphore(Supplier<T> action) {
        boolean permit = false;
        // TODO: use try with resources (autoclosable ?)
        try {
            permit = semaphore.tryAcquire(acquireMaxWaitDuration.getSeconds(), TimeUnit.SECONDS);
            if (permit) {
                return action.get();
            } else {
                log.warn("Could not acquire semaphore");
                throw new RuntimeException("Could not acquire semaphore");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        } finally {
            if (permit) {
                semaphore.release();
            }
        }
    }

    private ApiContext createApiConfig() throws UnknownHostException {
        ArrayList<String> permittedIps = new ArrayList<>();
        permittedIps.add("*");
        return ApiContext.create(
                environmentType,
                apiKey,
                InetAddress.getLocalHost().getHostName(),
                permittedIps
        );
    }

    /**
     *
     */
    private void setupContext() throws UnknownHostException {
        final boolean isSandboxEnvironment = SANDBOX.equals(environmentType);
        setupContext(isSandboxEnvironment ? 1 : 0);

        if (isSandboxEnvironment) {
            requestSpendingMoneyIfNeeded();
        }
    }

    /**
     *
     */
    private void setupContext(int retries) throws UnknownHostException {
        ApiContext apiContext;
        if (new File(determineBunqConfigFileName()).exists()) {
            log.info("Existing API config found. Restoring API context from file");
            apiContext = ApiContext.restore(determineBunqConfigFileName());
        } else if (SANDBOX.equals(environmentType)) {
            log.info("No API config found. Creating new sandbox API config.");
            apiContext = createSandboxApiContext();
        } else {
            log.info("No API config found. Creating new production API config.");
            apiContext = createApiConfig();
            log.info("Created new production API config.");
        }

        try {
            apiContext.ensureSessionActive();
            safeSave(apiContext);
            loadApiContext(apiContext);
        } catch (ApiException apiException) {
            if (retries > 0) {
                log.warn("Could not create API context. Will retry creating config", apiException);
                deleteOldConfig();
                setupContext(retries - 1);
            } else {
                throw apiException;
            }
        }
    }


    private void safeSave(ApiContext apiContext) {
        if (saveSessionToFile) {
            apiContext.save(determineBunqConfigFileName());
        } else {
            log.info("Skipping saving context to file");
        }
    }

    private String determineBunqConfigFileName() {
        return switch (environmentType) {
            case PRODUCTION -> FILE_NAME_BUNQ_CONF_PRODUCTION;
            case SANDBOX -> FILE_NAME_BUNQ_CONF_SANDBOX;
            case null -> FILE_NAME_BUNQ_CONF_SANDBOX;
        };
    }

    private void deleteOldConfig() {
        try {
            Files.delete(Paths.get((determineBunqConfigFileName())));
        } catch (IOException e) {
            throw new BunqException(e.getMessage());
        }
    }


}
