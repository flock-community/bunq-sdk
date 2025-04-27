package com.bunq.sdk;

import com.bunq.sdk.generated.endpoint.READ_User;
import com.bunq.sdk.generated.endpoint.List_all_MonetaryAccountBank_for_User;
import com.bunq.sdk.generated.model.UserPerson;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ApiTest {

    private static final Config config = new Config(
            "PeterScript",
            "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
    );

    @Test
    public void testApiCall() throws Exception {
        Signing signing = new Signing(config);
        Context context = Context.initContext(config);
        Client client = new Client(signing, context);

        READ_User.Request req = new READ_User.Request(
                context.getUserId(),
                Optional.empty(),
                config.getServiceName(),
                Optional.empty(),
                Optional.empty(),
                Optional.empty(),
                Optional.empty(),
                config.getApiKey()
        );

        READ_User.Response<?> res = client.rEAD_User(req).get();

        if (res instanceof READ_User.Response200 response) {
            assertEquals("Donald Byrne", response.getBody().UserPerson().flatMap(UserPerson::legal_name).orElseThrow());
        } else if (res instanceof READ_User.Response400) {
            throw new RuntimeException("Cannot read user");
        }
    }

    @Test
    public void testListAllMonetaryAccountBankForUser() throws Exception {
        Signing signing = new Signing(config);
        Context context = Context.initContext(config);
        Client client = new Client(signing, context);

        List_all_MonetaryAccountBank_for_User.Request req = new List_all_MonetaryAccountBank_for_User.Request(
                context.getUserId(),
                Optional.empty(),
                config.getServiceName(),
                Optional.empty(),
                Optional.empty(),
                Optional.empty(),
                Optional.empty(),
                context.getSessionToken()
        );

        List_all_MonetaryAccountBank_for_User.Response<?> res = client.list_all_MonetaryAccountBank_for_User(req).get();

        if (res instanceof List_all_MonetaryAccountBank_for_User.Response200 response) {
            assertEquals("D. Byrne", response.getBody().get(0).display_name());
        } else {
            throw new RuntimeException("Cannot list monetary accounts");
        }
    }
}