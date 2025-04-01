package org.example;

import com.bunq.sdk.model.generated.endpoint.MonetaryAccountBank;
import com.bunq.sdk.model.generated.endpoint.RequestInquiry;
import com.bunq.sdk.model.generated.object.Avatar;
import com.bunq.sdk.model.generated.object.MonetaryAccountProfileDrain;
import com.bunq.sdk.model.generated.object.MonetaryAccountProfileFill;
import community.flock.wirespec.generated.java.Amount;
import community.flock.wirespec.generated.java.BunqId;
import community.flock.wirespec.generated.java.CREATE_RequestInquiry_for_User_MonetaryAccount400ResponseBody;
import community.flock.wirespec.generated.java.CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint;
import community.flock.wirespec.generated.java.ErrorArray;
import community.flock.wirespec.generated.java.Image;
import community.flock.wirespec.generated.java.LabelMonetaryAccount;
import community.flock.wirespec.generated.java.MonetaryAccountBankRead;
import community.flock.wirespec.generated.java.MonetaryAccountProfile;
import community.flock.wirespec.generated.java.MonetaryAccountSetting;
import community.flock.wirespec.generated.java.Pointer;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_User400ResponseBody;
import community.flock.wirespec.generated.java.READ_MonetaryAccountBank_for_UserEndpoint;
import community.flock.wirespec.generated.java.RequestInquiryCreate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

import static java.util.Optional.empty;
import static java.util.Optional.ofNullable;

public class MonetaryAccountClientV1 implements READ_MonetaryAccountBank_for_UserEndpoint.Handler, CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Handler {
    private static final Logger logger = LoggerFactory.getLogger(MonetaryAccountClientV1.class);

    @Override
    public CompletableFuture<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>> rEAD_MonetaryAccountBank_for_User(READ_MonetaryAccountBank_for_UserEndpoint.Request request) {
        int accountId = Math.toIntExact(request.getPath().itemId());

        return CompletableFuture.supplyAsync(() -> MonetaryAccountBank.get(accountId).getValue())
                .<READ_MonetaryAccountBank_for_UserEndpoint.Response<?>>thenApply(it ->
                        new READ_MonetaryAccountBank_for_UserEndpoint.Response200(
                                empty(), // not-needed?
                                empty(), // not-needed?
                                empty(), // not-needed?
                                toMonetaryBankAccountRead(it))
                ).exceptionally(it -> {
                    logger.error("Something went wrong fetching MonetaryAccountBank with accountId {}", accountId, it);
                    return new READ_MonetaryAccountBank_for_UserEndpoint.Response400(
                            empty(), // not-needed?
                            empty(), // not-needed?
                            empty(), // not-needed?
                            to400Response(it));
                });
    }

    @Override
    public CompletableFuture<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>> cREATE_RequestInquiry_for_User_MonetaryAccount(CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Request request) {

        return CompletableFuture.supplyAsync(() ->
                        RequestInquiry.create(
                                toBunqAmount(request.getBody().amount_inquired()),
                                toBunqPointer(request.getBody().counterparty_alias()),
                                request.getBody().description().orElseThrow(),
                                request.getBody().allow_bunqme()
                        ).getValue())
                .<CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response<?>>thenApply(it ->
                        new CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response200(
                                Optional.empty(),
                                Optional.empty(),
                                Optional.empty(),
                                new RequestInquiryCreate(Optional.of(new BunqId(Optional.of(it.longValue()))))
                        )).exceptionally(it -> {
                    logger.error("Something went wrong requiring money", it);
                    return new CREATE_RequestInquiry_for_User_MonetaryAccountEndpoint.Response400(
                            empty(), // not-needed?
                            empty(), // not-needed?
                            empty(), // not-needed?
                            to400ResponseX(it));
                });
    }

    private com.bunq.sdk.model.generated.object.Pointer toBunqPointer(Optional<Pointer> counterPartyAlias) {
        Pointer pointer = counterPartyAlias.orElseThrow();
        return new com.bunq.sdk.model.generated.object.Pointer(
                pointer.type().orElseThrow(),
                pointer.value().orElseThrow(),
                pointer.name().orElse(null),
                pointer.service().orElse(null));


    }

    private com.bunq.sdk.model.generated.object.Amount toBunqAmount(Optional<Amount> amount) {
        Amount amount1 = amount.orElseThrow();
        return new com.bunq.sdk.model.generated.object.Amount(amount1.value().orElseThrow(), amount1.currency().orElseThrow());
    }

    private CREATE_RequestInquiry_for_User_MonetaryAccount400ResponseBody to400ResponseX(Throwable it) {
        return new CREATE_RequestInquiry_for_User_MonetaryAccount400ResponseBody(
                Optional.of(
                        List.of(
                                new ErrorArray(
                                        Optional.of(it.getMessage()),
                                        Optional.empty()
                                )
                        )
                )
        );
    }

    private READ_MonetaryAccountBank_for_User400ResponseBody to400Response(Throwable it) {
        return new READ_MonetaryAccountBank_for_User400ResponseBody(
                Optional.of(
                        List.of(
                                new ErrorArray(
                                        Optional.of(it.getMessage()),
                                        Optional.empty()
                                )
                        )
                )
        );
    }

    private MonetaryAccountBankRead toMonetaryBankAccountRead(MonetaryAccountBank it) {
        return new MonetaryAccountBankRead(ofNullable(it.getId()).map(id -> (long) id), // ID
                ofNullable(it.getCreated()), // Created
                ofNullable(it.getUpdated()), // Updated
                toAvatar(it.getAvatar()), // Avatar
                ofNullable(it.getCurrency()), // Currency
                ofNullable(it.getDescription()), // Description
                toAmount(it.getDailyLimit()), // Daily Limit
                toAmount(it.getOverdraftLimit()), // Overdraft Limit
                toAmount(it.getBalance()), // Balance
                toAliases(it.getAlias()), // Alias
                ofNullable(it.getPublicUuid()), // Public UUID
                ofNullable(it.getStatus()), // Status
                ofNullable(it.getSubStatus()), // Sub-status
                ofNullable(it.getReason()), // Reason
                ofNullable(it.getReasonDescription()), // Reason description
                ofNullable(it.getUserId()).map(id -> (long) id), // User ID
                toMonetaryAccountProfile(it.getMonetaryAccountProfile()), // Monetary Account Profile
                ofNullable(it.getDisplayName()), // Display Name
                toMonetaryAccountSetting(it.getSetting()), // Setting
                toAllAutoSaveId(it.getAllAutoSaveId()) // All Auto Save ID
        );
    }

    private Optional<List<BunqId>> toAllAutoSaveId(List<com.bunq.sdk.model.generated.object.BunqId> allAutoSaveId) {
        return ofNullable(allAutoSaveId).map(ids -> ids.stream().map(it -> new BunqId(ofNullable(it.getId()).map(id -> (long) id))).toList());
    }

    private Optional<MonetaryAccountSetting> toMonetaryAccountSetting(com.bunq.sdk.model.generated.object.MonetaryAccountSetting setting) {
        return ofNullable(setting).map(it -> new MonetaryAccountSetting(ofNullable(it.getColor()), ofNullable(it.getIcon()), ofNullable(it.getDefaultAvatarStatus()), ofNullable(it.getRestrictionChat()), ofNullable(it.getSddExpirationAction())));
    }

    private Optional<MonetaryAccountProfile> toMonetaryAccountProfile(com.bunq.sdk.model.generated.endpoint.MonetaryAccountProfile monetaryAccountProfile) {
        return ofNullable(monetaryAccountProfile).map(it -> new MonetaryAccountProfile(toProfileFill(it.getProfileFill()), toProfileDrain(it.getProfileDrain())));

    }

    private Optional<community.flock.wirespec.generated.java.MonetaryAccountProfileDrain> toProfileDrain(MonetaryAccountProfileDrain profileDrain) {
        return ofNullable(profileDrain).map(it -> new community.flock.wirespec.generated.java.MonetaryAccountProfileDrain(ofNullable(it.getStatus()), toAmount(it.getBalancePreferred()), toAmount(it.getBalanceThresholdHigh()), empty() // not filled by sdk?
        ));
    }

    private Optional<community.flock.wirespec.generated.java.MonetaryAccountProfileFill> toProfileFill(MonetaryAccountProfileFill profileFill) {
        return ofNullable(profileFill).map(it -> new community.flock.wirespec.generated.java.MonetaryAccountProfileFill(ofNullable(it.getStatus()), toAmount(it.getBalancePreferred()), toAmount(it.getBalanceThresholdLow()), empty() // not filled by sdk?
        ));

    }

    private Optional<List<Pointer>> toAliases(List<com.bunq.sdk.model.generated.object.Pointer> alias) {
        return ofNullable(alias).map(aliases -> aliases.stream().map(it -> new Pointer(ofNullable(it.getType()), ofNullable(it.getValue()), ofNullable(it.getName()), empty() // no service?
        )).toList());
    }

    private Optional<Amount> toAmount(com.bunq.sdk.model.generated.object.Amount dailyLimit) {
        return ofNullable(dailyLimit).map(it -> new Amount(ofNullable(it.getValue()), ofNullable(it.getCurrency())));
    }

    private Optional<community.flock.wirespec.generated.java.Avatar> toAvatar(Avatar avatar) {
        return ofNullable(avatar).map(it -> new community.flock.wirespec.generated.java.Avatar(ofNullable(it.getUuid()), ofNullable(it.getAnchorUuid()), toImage(it.getImage()), ofNullable(it.getStyle())));

    }

    private Optional<List<Image>> toImage(List<com.bunq.sdk.model.generated.object.Image> image) {
        return ofNullable(image).map(images -> images.stream().map(it -> new Image(ofNullable(it.getAttachmentPublicUuid()), ofNullable(it.getContentType()), ofNullable(it.getHeight()).map(id -> (long) id), ofNullable(it.getWidth()).map(id -> (long) id))).toList());

    }

}
