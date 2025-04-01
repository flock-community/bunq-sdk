package community.flock.bunq.java.example;

import community.flock.bunq.java.ContextInitializerHandler;
import community.flock.wirespec.generated.java.CREATE_DeviceServerEndpoint;
import community.flock.wirespec.generated.java.CREATE_InstallationEndpoint;
import community.flock.wirespec.generated.java.CREATE_SessionServerEndpoint;

import java.util.concurrent.CompletableFuture;

public class ContextInitializerHandlerImpl implements ContextInitializerHandler {
    @Override
    public CompletableFuture<CREATE_DeviceServerEndpoint.Response<?>> cREATE_DeviceServer(CREATE_DeviceServerEndpoint.Request request) {
        return null;
    }

    @Override
    public CompletableFuture<CREATE_InstallationEndpoint.Response<?>> cREATE_Installation(CREATE_InstallationEndpoint.Request request) {
        return null;
    }

    @Override
    public CompletableFuture<CREATE_SessionServerEndpoint.Response<?>> cREATE_SessionServer(CREATE_SessionServerEndpoint.Request request) {
        return null;
    }
}
