package community.flock.bunq.java.context;

import com.bunq.sdk.exception.BunqException;
import com.bunq.sdk.model.core.BunqModel;
import com.bunq.sdk.model.core.UserContextHelper;
import com.bunq.sdk.model.generated.endpoint.MonetaryAccountBank;
import com.bunq.sdk.model.generated.endpoint.UserApiKey;
import com.bunq.sdk.model.generated.endpoint.UserCompany;
import com.bunq.sdk.model.generated.endpoint.UserPaymentServiceProvider;
import com.bunq.sdk.model.generated.endpoint.UserPerson;

public class UserContext {
    /**
     * Error constants.
     */
    private static final String ERROR_UNEXPECTED_USER_INSTANCE = "\"%s\" is unexpected user instance.";
    private static final String ERROR_PRIMARY_MONETARY_ACCOUNT_IS_NOT_SET = "Primary monetaryAccount is not set";

    private final ApiContext apiContext;
    private UserCompany userCompany;
    private UserPerson userPerson;
    private UserApiKey userApiKey;
    private UserPaymentServiceProvider userPaymentServiceProvider;
    private MonetaryAccountBank primaryMonetaryAccountBank;

    public UserContext(ApiContext apiContext) {
        this.apiContext = apiContext;
        initUser(this.apiContext.getSessionContext().getUserReference());
    }

    private void initUser(BunqModel user) {
        if (user instanceof UserPerson) {
            this.userPerson = (UserPerson) user;
        } else if (user instanceof UserCompany) {
            this.userCompany = (UserCompany) user;
        } else if (user instanceof UserApiKey) {
            this.userApiKey = (UserApiKey) user;
        } else if (user instanceof UserPaymentServiceProvider) {
            this.userPaymentServiceProvider = (UserPaymentServiceProvider) user;
        } else {
            throw new BunqException(String.format(ERROR_UNEXPECTED_USER_INSTANCE, user.getClass().toString()));
        }
    }

    public void initMainMonetaryAccount(UserContextHelper helper) {
        if (this.userPaymentServiceProvider != null) {
            return;
        }

        this.primaryMonetaryAccountBank = helper.getFirstActiveMonetaryAccountBankByUserId(getUserId());
    }

    public void refreshContext() {
        UserContextHelper helper = new UserContextHelper(this.apiContext);
        this.initUser(helper.getFirstUser().getReferencedObject());
        this.initMainMonetaryAccount(helper);
    }

    public Integer getUserId() {
        return this.apiContext.getSessionContext().getUserId();
    }

    public boolean isOnlyUserPersonSet() {
        return this.userCompany == null && this.userApiKey == null && this.userPerson != null;
    }

    public boolean isOnlyUserCompanySet() {
        return this.userPerson == null && this.userApiKey == null && this.userCompany != null;
    }

    public boolean isOnlyUserApiKeySet() {
        return this.userPerson == null && this.userCompany == null && this.userApiKey != null;
    }

    public boolean areAllUserSet() {
        return this.userPerson != null && this.userCompany != null && this.userApiKey != null;
    }

    public Integer getMainMonetaryAccountId() {
        if (this.primaryMonetaryAccountBank == null) {
            throw new BunqException(ERROR_PRIMARY_MONETARY_ACCOUNT_IS_NOT_SET);
        } else {
            return this.primaryMonetaryAccountBank.getId();
        }
    }

    public UserPerson getUserPerson() {
        return this.userPerson;
    }

    public UserCompany getUserCompany() {
        return this.userCompany;
    }

    public UserApiKey getUserApiKey() {
        return userApiKey;
    }

    public MonetaryAccountBank getPrimaryMonetaryAccountBank() {
        return this.primaryMonetaryAccountBank;
    }
}
