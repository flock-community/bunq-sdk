package community.flock.bunq.java;

import community.flock.wirespec.generated.java.CREATE_DeviceServerEndpoint;
import community.flock.wirespec.generated.java.CREATE_InstallationEndpoint;
import community.flock.wirespec.generated.java.CREATE_SessionServerEndpoint;

public interface ContextInitializerHandler extends CREATE_InstallationEndpoint.Handler, CREATE_DeviceServerEndpoint.Handler, CREATE_SessionServerEndpoint.Handler {

}
